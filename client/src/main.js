import Vue from 'vue'
import VueCarousel from 'vue-carousel'
import VueAxios from 'vue-axios'
import App from './App.vue'
import ethConnect from "./eth.js";

var ethereumjsTx = require('ethereumjs-tx');
var ethereumjsAbi = require('ethereumjs-abi');
var ethereumjsWallet = require('ethereumjs-wallet');
var ethereumjsUtil = require('ethereumjs-util');
var axios = require('axios');

ethConnect().then(function(r) {
  var newWallet = ethereumjsWallet.generate();
  var newPrivateKey = newWallet.getPrivateKeyString();

  window.wasllet = newWallet;
  console.log(newWallet);

  var bidAmountInWei = 50000000000000000;
  var msgh = ethereumjsUtil.keccak256(bidAmountInWei);

  var sig = ethereumjsUtil.ecsign(
      ethereumjsUtil.toBuffer(msgh),
      ethereumjsUtil.toBuffer(newPrivateKey));

  var rpcSig = "0x" +
      ethereumjsUtil.setLengthLeft(sig.r, 32).toString("hex") +
      ethereumjsUtil.setLengthLeft(sig.s, 32).toString("hex") +
      ethereumjsUtil.toBuffer(sig.v).toString("hex");

  var addressCR = '0xa6e273458498b2642449e1ae1b57266e7db307b1';
  var addressAuction = '0x4cf2bfad89bc3a0a09533468040ed98336665772';



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
    });
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


console.log('axios=');
console.log(axios);

Vue.config.productionTip = false
Vue.use(VueCarousel)
Vue.prototype.$axios = axios

new Vue({
  render: h => h(App),
}).$mount('#app')
