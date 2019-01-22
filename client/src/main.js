import Vue from 'vue'
import VueCarousel from 'vue-carousel'
import VueAxios from 'vue-axios'
import App from './App.vue'
import ethConnect from "./eth.js";

var ethjsTx = require('ethereumjs-tx');
var ethjsAbi = require('ethereumjs-abi');
var ethjsWallet = require('ethereumjs-wallet');
var ethjsUtil = require('ethereumjs-util');
var axios = require('axios');
var fpsbApi = require('./api/api.js').default;

ethConnect().then(function(r) {

  //localStorage.removeItem('web3registered');
  //localStorage.removeItem('web3registered_privateKey');
  //localStorage.removeItem('web3registered_salt');

  if (!localStorage.web3registered) {
    var channelWallet = ethjsWallet.generate();
    var channelPrivateKey = channelWallet.getPrivateKeyString();
    var channelAddress = channelWallet.getAddressString();

    fpsbApi.registerSigningWallet(channelWallet);

    localStorage.setItem('web3registered', JSON.stringify(channelWallet))
    localStorage.setItem('web3registered_privateKey', channelWallet.getPrivateKeyString())
    localStorage.setItem('web3registered_address', channelWallet.getAddressString())
  }

  let bid = fpsbApi.constructSignedBid(500000000, ethjsUtil.toBuffer(localStorage.getItem('web3registered_privateKey')));
  console.log(web3.toHex(bid.hash));
  console.log(web3.toHex(bid.signature));
  console.log(localStorage.getItem('web3registered_address'));

  let channelAuctions = { addresses: [] };
  for (var i = 0; i < 10; i++) {
    fpsbApi.createAuction().then(function(response) {
      channelAuctions.addresses.push(response.data.address);
      localStorage.setItem('web3registered_auctions', JSON.stringify(channelAuctions))
    })
  }

  //var recoveredAddress = ethereumjsUtil.ecrecover(msgh, sig.v, sig.r, sig.s);

/*
  axios
    .get('http://127.0.0.1:5000/auction/abi')
    .then(r => {
      var abi = r.data.response;
      var ecr = ethereumjsUtil.ecrecover(msgh, sig.v, sig.r, sig.s);
      ecr = ethereumjsUtil.pubToAddress(ecr);
      var sign = ethereumjsUtil.toBuffer(rpcSig);
      var data = web3.eth.contract(abi).at(addressCR).commit(Array.from(msgh), Array.from(sign), addressAuction).sendTransaction({
        from: web3.eth.defaultAccount
      });
      console.log(ecr.toString("hex"));
    });*/

/*
  web3.eth.getTransactionCount(newWallet.getAddressString(), function (err, nonce) {
    var data = web3.eth.contract(abi).at(addressCR).commit.getData(msgh, rpcSig, addressAuction);
    var tx = new ethereumjs.Tx({
      nonce: nonce,
      gasPrice: web3.toHex(web3.toWei('20', 'gwei')),
      gasLimit: 100000,
      to: address,
      value: 0,
      data: data,
    });
    tx.sign(ethereumjs.Buffer.Buffer.from(newPrivateKey, 'hex'));
    var raw = '0x' + tx.serialize().toString('hex');
    web3.eth.sendRawTransaction(raw, function (err, transactionHash) {
      console.log(transactionHash);
    });
  });
*/
});

Vue.config.productionTip = false
Vue.use(VueCarousel)
Vue.prototype.$axios = axios

new Vue({
  render: h => h(App),
}).$mount('#app')
