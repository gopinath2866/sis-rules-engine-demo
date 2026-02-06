// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
AdapterRegistry — Final Kernel Implementation

This contract is a direct transcription of constitutional storage law.
It defines the enumerable, owner-controlled execution surface.

No upgrade paths. No inheritance. No discretion.
*/

contract AdapterRegistry {
    /*//////////////////////////////////////////////////////////////
                                STORAGE
    //////////////////////////////////////////////////////////////*/

    // Slot 0
    mapping(address => bool) public isAdapter;

    // Slot 1
    address public owner;

    /*//////////////////////////////////////////////////////////////
                                 EVENTS
    //////////////////////////////////////////////////////////////*/

    event AdapterAdded(address indexed adapter);
    event AdapterRemoved(address indexed adapter);

    /*//////////////////////////////////////////////////////////////
                                MODIFIER
    //////////////////////////////////////////////////////////////*/

    modifier onlyOwner() {
        require(msg.sender == owner, "INV_OWNER_ONLY");
        _;
    }

    /*//////////////////////////////////////////////////////////////
                              CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    constructor(address _owner) {
        require(_owner != address(0), "INV_OWNER_ZERO");
        owner = _owner;
    }

    /*//////////////////////////////////////////////////////////////
                         EXECUTION SURFACE CONTROL
    //////////////////////////////////////////////////////////////*/

    /**
     * addAdapter(adapter)
     *
     * Invariant:
     * only owner expands execution surface
     */
    function addAdapter(address adapter) external onlyOwner {
        require(adapter != address(0), "INV_ADAPTER_ZERO");
        require(!isAdapter[adapter], "INV_ADAPTER_EXISTS");

        isAdapter[adapter] = true;

        emit AdapterAdded(adapter);
    }

    /**
     * removeAdapter(adapter)
     *
     * Invariant:
     * execution surface can only shrink, never mutate silently
     */
    function removeAdapter(address adapter) external onlyOwner {
        require(isAdapter[adapter], "INV_ADAPTER_NOT_FOUND");

        isAdapter[adapter] = false;

        emit AdapterRemoved(adapter);
    }
}
