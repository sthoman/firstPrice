import json
import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))



# block explorer for the winners
indices = [0,1,2,3,4,5,6,7,8]
contractAddress = w3.toChecksumAddress('0xf4f4d478c585e356c9415e5fc2d9a61e9aeda227')
for x in indices:
  print(w3.eth.getStorageAt(contractAddress, x))
