import json
import web3

from web3 import Web3, HTTPProvider
from eth_account.messages import defunct_hash_message

# test calling on contract
w3 = Web3(HTTPProvider('http://localhost:8545'))

myAccount = w3.eth.account.create('test')

private_key = myAccount.privateKey;
msg = "hello"
message_hash = defunct_hash_message(text=msg)

#sig = w3.eth.sign(myAccount.address, messageHash)

sig = w3.eth.account.signHash(message_hash, private_key=private_key)

print(sig);

print (myAccount.address);

#signature = w3.toHex(sig)

#print(signature)
