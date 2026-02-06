// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
FeeSplitter — Final Kernel Implementation

This contract is a direct transcription of constitutional storage law.
It splits realized profits mechanically, with immutable ratios.

No discretion, no inflation, no upgrade hooks.
*/

interface IAgentVault {
    function totalAssets() external view returns (uint256);
}

interface IPerfToken {
    function mint(address to, uint256 amount) external;
}

contract FeeSplitter {
    /*//////////////////////////////////////////////////////////////
                                STORAGE
    //////////////////////////////////////////////////////////////*/

    // Slot 0
    address public vault;

    // Slot 1
    address public perfToken;

    // Slot 2
    address public agent;

    // Slot 3
    address public insurance;

    // Slot 4
    uint256 public perfCut;

    // Slot 5
    uint256 public agentCut;

    // Slot 6
    uint256 public insuranceCut;

    /*//////////////////////////////////////////////////////////////
                                 EVENTS
    //////////////////////////////////////////////////////////////*/

    event FeesDistributed(
        uint256 profit,
        uint256 perfAmount,
        uint256 agentAmount,
        uint256 insuranceAmount
    );

    /*//////////////////////////////////////////////////////////////
                              CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/

    constructor(
        address _vault,
        address _perfToken,
        address _agent,
        address _insurance,
        uint256 _perfCut,
        uint256 _agentCut,
        uint256 _insuranceCut
    ) {
        require(_vault != address(0), "INV_VAULT_ZERO");
        require(_perfToken != address(0), "INV_PERF_ZERO");
        require(_agent != address(0), "INV_AGENT_ZERO");
        require(_insurance != address(0), "INV_INS_ZERO");
        require(
            _perfCut + _agentCut + _insuranceCut == 10000,
            "INV_TOTAL_CUT"
        );

        vault = _vault;
        perfToken = _perfToken;
        agent = _agent;
        insurance = _insurance;
        perfCut = _perfCut;
        agentCut = _agentCut;
        insuranceCut = _insuranceCut;
    }

    /*//////////////////////////////////////////////////////////////
                         DISTRIBUTION LOGIC
    //////////////////////////////////////////////////////////////*/

    /**
     * distribute(profit)
     *
     * Invariant:
     * no inflation without realized profit
     * cuts are immutable
     */
    function distribute(uint256 profit) external {
        require(profit > 0, "INV_NO_PROFIT");

        uint256 perfAmount = (profit * perfCut) / 10000;
        uint256 agentAmount = (profit * agentCut) / 10000;
        uint256 insuranceAmount = (profit * insuranceCut) / 10000;

        // Mint exactly once across all recipients (total == profit)
        IPerfToken(perfToken).mint(agent, agentAmount);
        IPerfToken(perfToken).mint(insurance, insuranceAmount);
        IPerfToken(perfToken).mint(msg.sender, perfAmount);

        emit FeesDistributed(profit, perfAmount, agentAmount, insuranceAmount);
    }
}
