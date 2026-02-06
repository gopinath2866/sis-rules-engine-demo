// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
AgentVault — Final Kernel Implementation

This contract is a direct transcription of constitutional storage law.
No upgrade paths. No inheritance. No discretion.

Storage order, semantics, and invariants MUST match the prose exactly.
Any deviation is non-compliant, even if “functionally equivalent”.
*/

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

interface IEpochManager {
    function currentEpoch() external view returns (uint256);
    function epochs(uint256 epoch)
        external
        view
        returns (uint256 startBalance, uint256 endBalance, bool finalized);
}

interface IAdapterRegistry {
    function isAdapter(address adapter) external view returns (bool);
}

contract AgentVault {
    /*//////////////////////////////////////////////////////////////
                                STORAGE
    //////////////////////////////////////////////////////////////*/

    // Slot 0
    address public underlying;

    // Slot 1
    address public agent;

    // Slot 2
    address public epochManager;

    // Slot 3
    address public adapterRegistry;

    // Slot 4
    uint256 public totalShares;

    // Slot 5
    mapping(address => uint256) public shares;

    // Slot 6
    mapping(address => WithdrawRequest) public withdrawRequests;

    struct WithdrawRequest {
        uint256 shares;
        uint256 epoch;
    }

    /*//////////////////////////////////////////////////////////////
                                 EVENTS
    //////////////////////////////////////////////////////////////*/

    event Deposit(address indexed user, uint256 amount, uint256 sharesMinted);
    event WithdrawRequested(address indexed user, uint256 shares, uint256 epoch);
    event WithdrawFinalized(address indexed user, uint256 sharesBurned, uint256 amount);
    event AdapterCall(address indexed adapter, bytes4 selector);

    /*//////////////////////////////////////////////////////////////
                                MODIFIERS
    //////////////////////////////////////////////////////////////*/

    modifier onlyAgent() {
        require(msg.sender == agent, "INV_AGENT_ONLY");
        _;
    }

    /*//////////////////////////////////////////////////////////////
                              CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    constructor(
        address _underlying,
        address _agent,
        address _epochManager,
        address _adapterRegistry
    ) {
        require(_underlying != address(0), "INV_UNDERLYING_ZERO");
        require(_agent != address(0), "INV_AGENT_ZERO");
        require(_epochManager != address(0), "INV_EPOCH_ZERO");
        require(_adapterRegistry != address(0), "INV_REGISTRY_ZERO");

        underlying = _underlying;
        agent = _agent;
        epochManager = _epochManager;
        adapterRegistry = _adapterRegistry;
    }

    /*//////////////////////////////////////////////////////////////
                         EXTERNAL VIEW HELPERS
    //////////////////////////////////////////////////////////////*/

    function totalAssets() public view returns (uint256) {
        return IERC20(underlying).balanceOf(address(this));
    }

    /*//////////////////////////////////////////////////////////////
                          CORE VAULT FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    /**
     * deposit(amount)
     *
     * Invariant:
     * shares minted are a pure function of current NAV
     */
    function deposit(uint256 amount) external {
        require(amount > 0, "INV_ZERO_DEPOSIT");

        uint256 assetsBefore = totalAssets();
        uint256 sharesToMint;

        if (totalShares == 0) {
            // Initial depositor sets baseline
            sharesToMint = amount;
        } else {
            // Pure NAV-based minting
            sharesToMint = (amount * totalShares) / assetsBefore;
        }

        require(sharesToMint > 0, "INV_ZERO_SHARES");

        // Effects
        totalShares += sharesToMint;
        shares[msg.sender] += sharesToMint;

        // Interactions
        require(
            IERC20(underlying).transferFrom(msg.sender, address(this), amount),
            "INV_TRANSFER_FAIL"
        );

        emit Deposit(msg.sender, amount, sharesToMint);
    }

    /**
     * requestWithdraw(shares)
     *
     * Invariant:
     * withdrawal intent is immutable per epoch
     */
    function requestWithdraw(uint256 shareAmount) external {
        require(shareAmount > 0, "INV_ZERO_SHARES");
        require(shares[msg.sender] >= shareAmount, "INV_INSUFFICIENT_SHARES");

        uint256 current = IEpochManager(epochManager).currentEpoch();
        WithdrawRequest storage existing = withdrawRequests[msg.sender];

        // Immutable per epoch: cannot overwrite within same epoch
        if (existing.shares > 0) {
            require(existing.epoch != current, "INV_WITHDRAW_ALREADY_REQUESTED");
        }

        withdrawRequests[msg.sender] = WithdrawRequest({
            shares: shareAmount,
            epoch: current
        });

        emit WithdrawRequested(msg.sender, shareAmount, current);
    }

    /**
     * finalizeWithdraw(user)
     *
     * Invariant:
     * withdrawals only settle after epoch finalization
     */
    function finalizeWithdraw(address user) external {
        WithdrawRequest memory req = withdrawRequests[user];
        require(req.shares > 0, "INV_NO_WITHDRAW_REQUEST");

        (, , bool finalized) = IEpochManager(epochManager).epochs(req.epoch);
        require(finalized, "INV_EPOCH_NOT_FINAL");

        uint256 userShares = shares[user];
        require(userShares >= req.shares, "INV_SHARE_MISMATCH");

        uint256 assets = totalAssets();
        uint256 amountOut = (assets * req.shares) / totalShares;

        require(amountOut > 0, "INV_ZERO_WITHDRAW");

        // Effects
        shares[user] = userShares - req.shares;
        totalShares -= req.shares;
        delete withdrawRequests[user];

        // Interactions
        require(
            IERC20(underlying).transfer(user, amountOut),
            "INV_TRANSFER_FAIL"
        );

        emit WithdrawFinalized(user, req.shares, amountOut);
    }

    /**
     * adapterCall(adapter, data)
     *
     * Invariant:
     * vault only executes whitelisted adapter code
     */
    function adapterCall(address adapter, bytes calldata data) external onlyAgent {
        require(
            IAdapterRegistry(adapterRegistry).isAdapter(adapter),
            "INV_BAD_ADAPTER"
        );

        (bool ok, ) = adapter.call(data);
        require(ok, "INV_ADAPTER_CALL_FAIL");

        bytes4 selector;
        if (data.length >= 4) {
            selector = bytes4(data);
        }

        emit AdapterCall(adapter, selector);
    }
}
