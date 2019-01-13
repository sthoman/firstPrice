const w3 = require('web3');
const { generateMnemonic, EthHdWallet } = require('eth-hd-wallet');

var hdWallet = (function() {

  var self = {}, mnemonic = generateMnemonic(),
        wallet = EthHdWallet.fromMnemonic(mnemonic);

  var generateAddress = function() {
    return wallet.generateAddresses(1);
  }

  var generateHashedBid = function(bidAmount, salt) {
    var hashedBid = w3.utils.soliditySha3(
      {type: 'string', value: bidAmount },
      {type: 'string', value: salt }
    );
    return hashedBid;
  }

  self.generateAddress = generateAddress;
  self.generateHashedBid = generateHashedBid;
  return self;

}) ();

var bidCommit = hdWallet.generateHashedBid("5000", "dont_touch_my_salt");
console.log(bidCommit);
