const { expect } = require("chai");
const { ethers } = require("hardhat");
const { deployKernel } = require("./helpers/deployKernel.cjs");

describe("FeeSplitter", function () {
  let feeSplitter, agentVault, token, deployer, insurance, user1;

  beforeEach(async function () {
    const kernel = await deployKernel();
    feeSplitter = kernel.feeSplitter;
    agentVault = kernel.agentVault;
    token = kernel.token;
    deployer = kernel.deployer;
    insurance = kernel.insurance;
    user1 = kernel.user1;
  });

  it("should store immutable fee cuts", async function () {
    expect(await feeSplitter.perfCut()).to.equal(5000);
    expect(await feeSplitter.agentCut()).to.equal(3000);
    expect(await feeSplitter.insuranceCut()).to.equal(2000);
  });

  it("should have correct constructor references", async function () {
    expect(await feeSplitter.vault()).to.equal(await agentVault.getAddress());
    expect(await feeSplitter.perfToken()).to.equal(await token.getAddress());
    expect(await feeSplitter.agent()).to.equal(deployer.address);
    expect(await feeSplitter.insurance()).to.equal(insurance.address);
  });

  it("should mint exactly profit across recipients", async function () {
    const profit = ethers.parseUnits("100", 18);
    const supplyBefore = await token.totalSupply();
    const agentBefore = await token.balanceOf(deployer.address);
    const insuranceBefore = await token.balanceOf(insurance.address);
    const callerBefore = await token.balanceOf(user1.address);

    await expect(feeSplitter.connect(user1).distribute(profit)).to.not.be.reverted;

    const supplyAfter = await token.totalSupply();
    const agentAfter = await token.balanceOf(deployer.address);
    const insuranceAfter = await token.balanceOf(insurance.address);
    const callerAfter = await token.balanceOf(user1.address);

    const perfAmount = (profit * 5000n) / 10000n;
    const agentAmount = (profit * 3000n) / 10000n;
    const insuranceAmount = (profit * 2000n) / 10000n;

    expect(supplyAfter - supplyBefore).to.equal(profit);
    expect(agentAfter - agentBefore).to.equal(agentAmount);
    expect(insuranceAfter - insuranceBefore).to.equal(insuranceAmount);
    expect(callerAfter - callerBefore).to.equal(perfAmount);
  });
});
