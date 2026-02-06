// test/check-all-signers.test.cjs
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Check All Signers", function () {
  it("should list all available signers", async function () {
    const signers = await ethers.getSigners();
    console.log(`Total signers available: ${signers.length}`);
    
    for (let i = 0; i < signers.length; i++) {
      console.log(`Signer ${i}: ${signers[i].address}`);
    }
    
    // Hardhat should give us 20 signers by default
    expect(signers.length).to.be.greaterThanOrEqual(5);
  });
});