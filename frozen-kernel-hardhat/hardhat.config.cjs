require("@nomicfoundation/hardhat-chai-matchers");
require("@nomicfoundation/hardhat-ethers");

module.exports = {
  solidity: "0.8.21",
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      chainId: 1337,
      accounts: [
        // Keep your existing accounts
        { privateKey: "0x59c6995e998f97a5a0044966f0945388d6a0e2e79ca1bb7c0a3c4c7e7f85d1d5", balance: "10000000000000000000000" },
        { privateKey: "0x8b3a350cf5c34c9194ca1b6d38bcf5da3c0b7e7b2a11199cbb6a94c434c55df2", balance: "10000000000000000000000" },
        // Add 3 more accounts for testing
        { privateKey: "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80", balance: "10000000000000000000000" },
        { privateKey: "0xde9be858da4a475276426320d5e9262ecfc3ba460bfac56360bfa6c4c28b4ee0", balance: "10000000000000000000000" },
        { privateKey: "0xdf57089febbacf7ba0bc227dafbffa9fc08a93fdc68e1e42411a14efcf23656e", balance: "10000000000000000000000" }
      ]
    }
  }
};