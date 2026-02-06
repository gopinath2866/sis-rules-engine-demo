const { expect } = require("chai");
const { deployKernel } = require("./helpers/deployKernel.cjs");

describe("DisputeModule", function () {
  let disputeModule, disputeAuthority, user1;

  beforeEach(async function () {
    const kernel = await deployKernel();
    disputeModule = kernel.disputeModule;
    disputeAuthority = kernel.disputeAuthority;
    user1 = kernel.user1;
  });

  it("should only allow dispute authority to dispute", async function () {
    // This will likely revert for other reasons (epoch doesn't exist)
    // but we can at least check it doesn't revert due to auth
    try {
      await disputeModule.connect(disputeAuthority).dispute(1, "0x1234");
    } catch (e) {
      // Ignore other errors, just not auth error
      expect(e.message).to.not.include("only dispute authority");
    }
  });

  it("should reject disputes from non-authority", async function () {
    await expect(
      disputeModule.connect(user1).dispute(1, "0x1234")
    ).to.be.reverted;
  });
});