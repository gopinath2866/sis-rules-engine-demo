const { expect } = require("chai");
const { ethers } = require("hardhat");
const { deployKernel } = require("./helpers/deployKernel.cjs");

describe("Debug", function () {
  it("should deploy everything", async function () {
    console.log("Starting deployment test...");
    const kernel = await deployKernel();
    
    console.log("\n=== Deployment Results ===");
    console.log("Deployer:", kernel.deployer.address);
    console.log("User1:", kernel.user1.address);
    console.log("Insurance:", kernel.insurance.address);
    console.log("DisputeAuthority:", kernel.disputeAuthority.address);
    console.log("ExecutorSigner:", kernel.executorSigner.address);
    console.log("Token:", await kernel.token.getAddress());
    console.log("AdapterRegistry:", await kernel.adapterRegistry.getAddress());
    console.log("AgentVault:", await kernel.agentVault.getAddress());
    console.log("EpochManager:", await kernel.epochManager.getAddress());
    console.log("ReceiptRegistry:", await kernel.receiptRegistry.getAddress());
    console.log("FeeSplitter:", await kernel.feeSplitter.getAddress());
    console.log("DisputeModule:", await kernel.disputeModule.getAddress());
    
    // Verify everything is deployed
    expect(kernel.deployer.address).to.not.be.undefined;
    expect(await kernel.token.getAddress()).to.not.equal(ethers.ZeroAddress);
  });
});