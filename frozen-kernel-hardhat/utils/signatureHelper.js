const { ethers } = require("hardhat");

module.exports = {
  signReceipt: async (signer, receipt) => {
    const digest = ethers.keccak256(
      ethers.AbiCoder.defaultAbiCoder().encode(
        ["uint256","bytes32","bytes32","uint256","uint256","uint256","uint256","address"],
        [
          receipt.epoch,
          receipt.strategyHash,
          receipt.actionHash,
          receipt.balanceBefore,
          receipt.balanceAfter,
          receipt.gasUsed,
          receipt.timestamp,
          receipt.executor
        ]
      )
    );

    return await signer.signMessage(ethers.getBytes(digest));
  }
};
