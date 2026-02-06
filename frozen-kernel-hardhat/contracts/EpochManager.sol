// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
EpochManager — Final Kernel Implementation

This contract is a direct transcription of constitutional storage law.
It fixes epoch boundaries and immutable balance snapshots.

No upgrade paths. No inheritance. No discretion.
*/

interface IAgentVault {
    function totalAssets() external view returns (uint256);
}

contract EpochManager {
    /*//////////////////////////////////////////////////////////////
                                STORAGE
    //////////////////////////////////////////////////////////////*/

    // Slot 0
    uint256 public currentEpoch;

    // Slot 1
    address public vault;

    // Slot 2
    mapping(uint256 => EpochSnapshot) public epochs;

    struct EpochSnapshot {
        uint256 startBalance;
        uint256 endBalance;
        bool finalized;
        bool started;
    }

    /*//////////////////////////////////////////////////////////////
                                 EVENTS
    //////////////////////////////////////////////////////////////*/

    event EpochStarted(uint256 indexed epoch, uint256 startBalance);
    event EpochFinalized(uint256 indexed epoch, uint256 endBalance);

    /*//////////////////////////////////////////////////////////////
                              CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    constructor(address _vault) {
        require(_vault != address(0), "INV_VAULT_ZERO");
        vault = _vault;
        currentEpoch = 0;
    }

    /*//////////////////////////////////////////////////////////////
                          CORE EPOCH FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    /**
     * startEpoch()
     *
     * Invariant:
     * snapshot reflects vault state at epoch start
     */
    function startEpoch() external {
        EpochSnapshot storage snap = epochs[currentEpoch];

        // Cannot start an epoch twice
        require(
            !snap.started && snap.finalized == false,
            "INV_EPOCH_ALREADY_STARTED"
        );

        uint256 balance = IAgentVault(vault).totalAssets();
        snap.startBalance = balance;
        snap.started = true;

        emit EpochStarted(currentEpoch, balance);
    }

    /**
     * finalizeEpoch()
     *
     * Invariant:
     * snapshot reflects vault state at epoch end and becomes immutable
     */
    function finalizeEpoch() external {
        EpochSnapshot storage snap = epochs[currentEpoch];

        require(snap.started, "INV_EPOCH_NOT_STARTED");
        require(!snap.finalized, "INV_EPOCH_ALREADY_FINAL");

        uint256 balance = IAgentVault(vault).totalAssets();
        snap.endBalance = balance;
        snap.finalized = true;

        emit EpochFinalized(currentEpoch, balance);

        // Advance epoch counter — monotonic, irreversible
        currentEpoch += 1;
    }
}
