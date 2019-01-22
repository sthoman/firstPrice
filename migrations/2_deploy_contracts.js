var fpsbAuctionContract = artifacts.require("./FPSBAuction.sol");
var fpsbSealedCommitReveal = artifacts.require("./SealedCR.sol");
var fpsbSealedCommitRevealAuction = artifacts.require("./SealedAuction.sol");

module.exports = function(deployer) {
  deployer.deploy(fpsbAuctionContract).then(function() {
  });
  deployer.deploy(fpsbSealedCommitReveal).then(function() {
  });
  deployer.deploy(fpsbSealedCommitRevealAuction).then(function() {
  });
};
