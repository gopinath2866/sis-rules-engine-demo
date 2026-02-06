// test/helpers/deployKernel.cjs
const { ethers } = require("hardhat");

async function deployKernel() {
  try {
    console.log("Getting signers...");
    // Get ALL signers (Hardhat provides 20 by default)
    const signers = await ethers.getSigners();
    console.log("Number of signers available:", signers.length);
    
    // Use the first 5 signers
    if (signers.length < 5) {
      throw new Error(`Need at least 5 signers, but only got ${signers.length}`);
    }
    
    const deployer = signers[0];
    const user1 = signers[1];
    const insurance = signers[2];
    const disputeAuthority = signers[3];
    const executorSigner = signers[4];

    console.log("Using signers:", {
      deployer: deployer.address,
      user1: user1.address,
      insurance: insurance.address,
      disputeAuthority: disputeAuthority.address,
      executorSigner: executorSigner.address
    });

    // Rest of your deployment code remains the same...
    // TestToken
    console.log("Deploying TestToken...");
    const TestToken = await ethers.getContractFactory("TestToken");
    const token = await TestToken.deploy(ethers.parseUnits("1000000", 18));
    await token.waitForDeployment();
    const tokenAddress = await token.getAddress();

    // AdapterRegistry
    console.log("Deploying AdapterRegistry...");
    const AdapterRegistry = await ethers.getContractFactory("AdapterRegistry");
    const adapterRegistry = await AdapterRegistry.deploy(deployer.address);
    await adapterRegistry.waitForDeployment();

    // AgentVault
    console.log("Deploying AgentVault...");
    const AgentVault = await ethers.getContractFactory("AgentVault");
    const agentVault = await AgentVault.deploy(
      tokenAddress,
      deployer.address,
      deployer.address, // Temporary EpochManager
      await adapterRegistry.getAddress()
    );
    await agentVault.waitForDeployment();
    const agentVaultAddress = await agentVault.getAddress();

    // EpochManager
    console.log("Deploying EpochManager...");
    const EpochManager = await ethers.getContractFactory("EpochManager");
    const epochManager = await EpochManager.deploy(agentVaultAddress);
    await epochManager.waitForDeployment();

    // ReceiptRegistry
    console.log("Deploying ReceiptRegistry...");
    const ReceiptRegistry = await ethers.getContractFactory("ReceiptRegistry");
    const receiptRegistry = await ReceiptRegistry.deploy(
      executorSigner.address,
      await epochManager.getAddress()
    );
    await receiptRegistry.waitForDeployment();

    // FeeSplitter
    console.log("Deploying FeeSplitter...");
    const FeeSplitter = await ethers.getContractFactory("FeeSplitter");
    const feeSplitter = await FeeSplitter.deploy(
      agentVaultAddress,
      tokenAddress,
      deployer.address,
      insurance.address,
      5000,
      3000,
      2000
    );
    await feeSplitter.waitForDeployment();

    // DisputeModule
    console.log("Deploying DisputeModule...");
    const DisputeModule = await ethers.getContractFactory("DisputeModule");
    const disputeModule = await DisputeModule.deploy(
      await receiptRegistry.getAddress(),
      disputeAuthority.address
    );
    await disputeModule.waitForDeployment();

    console.log("All deployments completed successfully!");

    return {
      deployer,
      user1,
      insurance,
      disputeAuthority,
      executorSigner,
      token,
      adapterRegistry,
      agentVault,
      epochManager,
      receiptRegistry,
      feeSplitter,
      disputeModule,
    };
  } catch (error) {
    console.error("Error in deployKernel:", error.message);
    throw error;
  }
}

module.exports = { deployKernel };