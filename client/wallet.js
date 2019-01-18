const fs = require('fs');
const Web3 = require('web3');
const ethUtil = require('ethereumjs-util');
const path = require("path");
const { generateMnemonic, EthHdWallet } = require('eth-hd-wallet');

web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:8545"));
web3.eth.defaultAccount = web3.eth.accounts[0];

var hdWallet = (function() {

  var self = {}, mnemonic = generateMnemonic(),
        wallet = EthHdWallet.fromMnemonic(mnemonic);

  var generateAddress = function() {
    return wallet.generateAddresses(1);
  }

  var generateHashedBid = function(bidAmount, salt) {
    var hashedBid = web3.utils.soliditySha3(
      {type: 'string', value: bidAmount },
      {type: 'string', value: salt }
    );
    return hashedBid;
  }

  var getContractAbi = function() {
    var file = fs.readFileSync(path.resolve(__dirname, "contracts/SealedCR.json"));
    var parsed = JSON.parse(file);
    var abi = parsed.abi;
    var addr = getContractAddress();

    console.log(addr);

    var YourContract = new web3.eth.Contract(abi, addr);
    console.log(YourContract);
  }

  var getContractAddress = function() {
    //  Method to rely on the deterministic deployment address, kind of
    //  like what enables counterfactual instantiation
    var deployerAccount = web3.eth.defaultAccount;
    var counterfactualAddress = ethUtil.bufferToHex(ethUtil.generateAddress(
        deployerAccount,
          web3.eth.getTransactionCount(deployerAccount)
    ));
    return counterfactualAddress;
    //  Deploy
    //TODO
  }

  self.getContractAbi = getContractAbi;
  self.generateAddress = generateAddress;
  self.generateHashedBid = generateHashedBid;
  return self;

}) ();

console.log(web3.eth.getAccounts().then(function(res) {
    console.log(res);
})); 
hdWallet.getContractAbi();
//var eventListener = generateEventListener();
//console.log(eventListener);

//var bidCommit = hdWallet.generateHashedBid("5000", "dont_touch_my_salt");
//console.log(bidCommit);
