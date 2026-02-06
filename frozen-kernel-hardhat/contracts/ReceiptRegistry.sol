// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
ReceiptRegistry — Final Kernel Implementation

This contract is a direct transcription of constitutional storage law.
It records append-only claims and enforces irreversible freezing.

Receipts are claims, not truth.
Freezing is terminal.
*/

interface IEpochManager {
    function currentEpoch() external view returns (uint256);
}

contract ReceiptRegistry {
    /*//////////////////////////////////////////////////////////////
                                STORAGE
    //////////////////////////////////////////////////////////////*/

    // Slot 0
    mapping(uint256 => Receipt) public receipts;

    // Slot 1
    address public executorSigner;

    // Slot 2
    address public epochManager;

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

    /*//////////////////////////////////////////////////////////////
                                 EVENTS
    //////////////////////////////////////////////////////////////*/

    event ReceiptSubmitted(uint256 indexed epoch, address indexed executor);
    event ReceiptFrozen(uint256 indexed epoch);

    /*//////////////////////////////////////////////////////////////
                              CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    constructor(address _executorSigner, address _epochManager) {
        require(_executorSigner != address(0), "INV_SIGNER_ZERO");
        require(_epochManager != address(0), "INV_EPOCH_ZERO");

        executorSigner = _executorSigner;
        epochManager = _epochManager;
    }

    /*//////////////////////////////////////////////////////////////
                         RECEIPT SUBMISSION LOGIC
    //////////////////////////////////////////////////////////////*/

    /**
     * submitReceipt(epoch, receipt, signature)
     *
     * Invariant:
     * one receipt per epoch, signature-bound
     */
    function submitReceipt(
        uint256 epoch,
        Receipt calldata r,
        bytes calldata signature
    ) external {
        Receipt storage existing = receipts[epoch];
        require(existing.executor == address(0), "INV_RECEIPT_EXISTS");

        // Epoch validity: cannot claim future epoch
        uint256 current = IEpochManager(epochManager).currentEpoch();
        require(epoch < current, "INV_EPOCH_NOT_FINAL");

        // Receipt must self-identify its epoch
        require(r.epoch == epoch, "INV_EPOCH_MISMATCH");

        // Verify signature binds receipt to executorSigner
        require(_verify(r, signature), "INV_BAD_SIGNATURE");

        receipts[epoch] = r;

        emit ReceiptSubmitted(epoch, r.executor);
    }

    /**
     * freeze(epoch)
     *
     * Invariant:
     * frozen receipts cannot be superseded
     */
    function freeze(uint256 epoch) external {
        Receipt storage r = receipts[epoch];
        require(r.executor != address(0), "INV_NO_RECEIPT");
        require(!r.frozen, "INV_ALREADY_FROZEN");

        r.frozen = true;

        emit ReceiptFrozen(epoch);
    }

    /*//////////////////////////////////////////////////////////////
                         SIGNATURE VERIFICATION
    //////////////////////////////////////////////////////////////*/

    function _verify(
        Receipt calldata r,
        bytes calldata signature
    ) internal view returns (bool) {
        bytes32 digest = keccak256(
            abi.encode(
                r.epoch,
                r.strategyHash,
                r.actionHash,
                r.balanceBefore,
                r.balanceAfter,
                r.gasUsed,
                r.timestamp,
                r.executor
            )
        );

        bytes32 ethSigned = keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", digest)
        );

        (bytes32 rSig, bytes32 sSig, uint8 vSig) = _split(signature);
        address recovered = ecrecover(ethSigned, vSig, rSig, sSig);

        return recovered == executorSigner;
    }

    function _split(
        bytes calldata sig
    ) internal pure returns (bytes32 r, bytes32 s, uint8 v) {
        require(sig.length == 65, "INV_SIG_LENGTH");

        assembly {
            r := calldataload(sig.offset)
            s := calldataload(add(sig.offset, 32))
            v := byte(0, calldataload(add(sig.offset, 64)))
        }
    }
}
