var fs = require('fs')
var fpsbAuctionContract = artifacts.require("./FPSBAuction.sol");


//TODO create auction contract registry to manage contract deployment
module.exports = function(deployer) {
  deployer.deploy(fpsbAuctionContract).then(function() {
    fs.writeFile("address.txt", fpsbAuctionContract.address, function(err) {
    });
  });
};
