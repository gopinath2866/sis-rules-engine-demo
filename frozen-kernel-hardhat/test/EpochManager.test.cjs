const { expect } = require("chai");
const { ethers } = require("hardhat");
const { deployKernel } = require("./helpers/deployKernel.cjs");

describe("EpochManager", function () {
  let epochManager;

  beforeEach(async function () {
    const kernel = await deployKernel();
    epochManager = kernel.epochManager;
  });

  it("should start at epoch 0", async function () {
    expect(await epochManager.currentEpoch()).to.equal(0);
  });

  it("should have a vault address", async function () {
    expect(await epochManager.vault()).to.not.equal(ethers.ZeroAddress);
  });

  it("should allow finalize after an empty epoch", async function () {
    await expect(epochManager.startEpoch()).to.not.be.reverted;
    await expect(epochManager.finalizeEpoch()).to.not.be.reverted;

    expect(await epochManager.currentEpoch()).to.equal(1);

    const snap = await epochManager.epochs(0);
    expect(snap[0]).to.equal(0);
    expect(snap[1]).to.equal(0);
    expect(snap[2]).to.equal(true);
    expect(snap[3]).to.equal(true);
  });
});
