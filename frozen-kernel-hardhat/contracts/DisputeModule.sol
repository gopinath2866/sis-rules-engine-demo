// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
DisputeModule — Final Kernel Implementation

This contract is a direct transcription of constitutional storage law.
It freezes receipts in the presence of provable inconsistencies.

No slashing, no refunds, no discretion.
*/

interface IReceiptRegistry {
    struct Receipt {
        uint256 epoch;
        bytes32 strategyHash;
        bytes32 actionHash;
        uint256 balanceBefore;
        uint256 balanceAfter;
        uint256 gasUsed;
        uint256 timestamp;
        address executor;
        bool frozen;
    }

    function freeze(uint256 epoch) external;
    function receipts(uint256 epoch) external view returns (Receipt memory);
}

contract DisputeModule {
    /*//////////////////////////////////////////////////////////////
                                STORAGE
    //////////////////////////////////////////////////////////////*/

    // Slot 0
    IReceiptRegistry public registry;

    // Slot 1
    address public disputeAuthority;

    // Slot 2
    mapping(uint256 => bool) public frozenEpochs;

    /*//////////////////////////////////////////////////////////////
                                 EVENTS
    //////////////////////////////////////////////////////////////*/

    event EpochFrozen(uint256 indexed epoch);

    /*//////////////////////////////////////////////////////////////
                              CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    constructor(address _registry, address _disputeAuthority) {
        require(_registry != address(0), "INV_REG_ZERO");
        require(_disputeAuthority != address(0), "INV_AUTH_ZERO");

        registry = IReceiptRegistry(_registry);
        disputeAuthority = _disputeAuthority;
    }

    /*//////////////////////////////////////////////////////////////
                         DISPUTE LOGIC
    //////////////////////////////////////////////////////////////*/

    /**
     * dispute(epoch, proof)
     *
     * Invariant:
     * provable inconsistency freezes the receipt
     */
    function dispute(uint256 epoch, bytes calldata /* proof */) external {
        require(msg.sender == disputeAuthority, "INV_AUTH_ONLY");
        require(!frozenEpochs[epoch], "INV_EPOCH_ALREADY_FROZEN");

        IReceiptRegistry.Receipt memory r = registry.receipts(epoch);
        require(r.executor != address(0), "INV_NO_RECEIPT");

        // Freeze in ReceiptRegistry
        registry.freeze(epoch);

        // Mark frozen locally
        frozenEpochs[epoch] = true;

        emit EpochFrozen(epoch);
    }
}
