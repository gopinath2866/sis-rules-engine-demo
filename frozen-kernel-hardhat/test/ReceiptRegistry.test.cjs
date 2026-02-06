const { expect } = require("chai");
const { ethers } = require("hardhat");
const { deployKernel } = require("./helpers/deployKernel.cjs");

describe("ReceiptRegistry", function () {
  let receiptRegistry, executorSigner, epochManager;

  beforeEach(async function () {
    const kernel = await deployKernel();
    receiptRegistry = kernel.receiptRegistry;
    executorSigner = kernel.executorSigner;
    epochManager = kernel.epochManager;
  });

  it("should have correct constructor references", async function () {
    expect(await receiptRegistry.executorSigner()).to.equal(executorSigner.address);
    expect(await receiptRegistry.epochManager()).to.equal(await epochManager.getAddress());
  });

  it("should reject invalid signatures", async function () {
    // Create proper 32-byte hashes (0x + 64 hex characters = 32 bytes)
    const strategyHash = "0x" + "1".repeat(64); // 32 bytes
    const actionHash = "0x" + "2".repeat(64);   // 32 bytes
    
    // Create a proper receipt struct that matches the contract
    const receiptData = [
      1,                          // epoch (uint256)
      strategyHash,               // strategyHash (bytes32)
      actionHash,                 // actionHash (bytes32)
      0,                          // balanceBefore (uint256)
      0,                          // balanceAfter (uint256)
      0,                          // gasUsed (uint256)
      Math.floor(Date.now() / 1000), // timestamp (uint256)
      executorSigner.address,     // executor (address)
      false                       // frozen (bool)
    ];

    // Create an invalid signature (just random bytes)
    const invalidSignature = "0x" + "00".repeat(65); // 65 bytes for ECDSA
    
    // This should revert because signature is invalid
    await expect(
      receiptRegistry.submitReceipt(1, receiptData, invalidSignature)
    ).to.be.reverted;
  });
});