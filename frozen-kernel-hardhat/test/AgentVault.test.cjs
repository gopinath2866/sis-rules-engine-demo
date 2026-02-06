const { expect } = require("chai");
const { ethers } = require("hardhat");
const { deployKernel } = require("./helpers/deployKernel.cjs");

describe("AgentVault", function () {
  let agentVault, token, deployer, user1;

  beforeEach(async function () {
    const kernel = await deployKernel();
    agentVault = kernel.agentVault;
    token = kernel.token;
    deployer = kernel.deployer;
    user1 = kernel.user1;
  });

  it("should have correct constructor references", async function () {
    expect(await agentVault.underlying()).to.equal(await token.getAddress());
    expect(await agentVault.agent()).to.equal(deployer.address);
  });

  it("should accept deposits when approved", async function () {
    const amount = ethers.parseUnits("100", 18);
    await token.approve(await agentVault.getAddress(), amount);
    await expect(agentVault.deposit(amount)).to.not.be.reverted;
  });

  it("should reject deposits without approval", async function () {
    const amount = ethers.parseUnits("100", 18);
    await expect(agentVault.deposit(amount)).to.be.reverted;
  });
});