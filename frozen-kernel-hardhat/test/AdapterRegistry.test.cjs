const { expect } = require("chai");
const { deployKernel } = require("./helpers/deployKernel.cjs");

describe("AdapterRegistry", function () {
  let adapterRegistry, deployer, user1;

  beforeEach(async function () {
    const kernel = await deployKernel();
    adapterRegistry = kernel.adapterRegistry;
    deployer = kernel.deployer;
    user1 = kernel.user1;
  });

  it("should allow only owner to add adapters", async function () {
    const addr = user1.address;
    await adapterRegistry.connect(deployer).addAdapter(addr);
    expect(await adapterRegistry.isAdapter(addr)).to.be.true;

    await expect(
      adapterRegistry.connect(user1).addAdapter(addr)
    ).to.be.revertedWith("INV_OWNER_ONLY");
  });

  it("should remove adapters correctly", async function () {
    const addr = user1.address;
    await adapterRegistry.connect(deployer).addAdapter(addr);
    await adapterRegistry.connect(deployer).removeAdapter(addr);
    expect(await adapterRegistry.isAdapter(addr)).to.be.false;
  });
});
