var axios = require('axios');
var ethjsTx = require('ethereumjs-tx');
var ethjsAbi = require('ethereumjs-abi');
var ethjsWallet = require('ethereumjs-wallet');
var ethjsUtil = require('ethereumjs-util');

var fpsbApi = (function (self, $provider, API_URI) {

  // constructSignedBid
  // Combines an amount in WEI with a random salt, and signs
  // it using the delegated account
  function constructSignedBid(amountInWei, privateKey) {

    var salt = new Uint8Array(16);
    crypto.getRandomValues(salt);

    var msgh = ethjsUtil.keccak256(amountInWei);//+ salt);
    var sig = ethjsUtil.ecsign(ethjsUtil.toBuffer(msgh), privateKey);
    var rpcSig = "0x" +
        ethjsUtil.setLengthLeft(sig.r, 32).toString("hex") +
        ethjsUtil.setLengthLeft(sig.s, 32).toString("hex") +
        ethjsUtil.toBuffer(sig.v).toString("hex");

    localStorage.setItem('web3registered_salt', salt);

    console.log("msgh=");
    console.log(msgh);
    console.log('signature=');
    console.log(ethjsUtil.toBuffer(rpcSig));

    return { hash: msgh, signature: ethjsUtil.toBuffer(rpcSig) };
  }

  // registerSigningWallet
  // This function allows any MetaMask user to generate a new
  // address and delegate that address to sign on their behalf
  // through the state channel.
  function registerSigningWallet(wallet) {
    console.log('about to register wallet=');
    console.log(wallet);
    $provider
      .post(API_URI.concat('/commits/register'))
      .then(response => {
        var signingAddress = wallet.getAddressString();
        var commitsAddress = response.data.address;
        var abi = response.data.abi;
        setTimeout(function() {
          var data = web3.eth.contract(abi).at(commitsAddress).register(signingAddress).sendTransaction({
            from: web3.eth.defaultAccount,
            gas: 100000,
            gasLimit: 100000
          });
        }, 1000);
      });
  }

  // sendBidFromWallet
  // Send a bid to an auction, signed via the new wallet
  // designated to sign on users' behalf
  function sendBidFromWallet(hash, signature, auctionAddress) {
    $provider.put(API_URI.concat('/commits/bid'), {
        params: {
            bid: hash,
            sig: signature,
            auction_address: auctionAddress
        }
    });
  }

  // createAuctions
  // Functionality to create auctions from the client side
  // (in bulk) for now, to test the architecture
  function createAuction() {
    return $provider.put(API_URI.concat('/auction/create'));
  }

  self.constructSignedBid = constructSignedBid;
  self.registerSigningWallet = registerSigningWallet;
  self.sendBidFromWallet = registerSigningWallet;
  self.createAuction = createAuction;
  return self;

}( {}, axios, 'http://127.0.0.1:5000'))

export default fpsbApi;
