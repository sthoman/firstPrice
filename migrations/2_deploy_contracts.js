var fpsbAuctionContract = artifacts.require("./FPSBAuction.sol");

module.exports = function(deployer) {
  deployer.deploy(fpsbAuctionContract);
};
