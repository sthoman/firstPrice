const { generateMnemonic, EthHdWallet } = require('eth-hd-wallet')

const wallet = EthHdWallet.fromMnemonic(generateMnemonic())

console.log( wallet instanceof EthHdWallet ); /* true */

console.log( wallet.generateAddresses(2) )
