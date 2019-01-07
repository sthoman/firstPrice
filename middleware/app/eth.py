import json
import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.defaultAccount = w3.eth.accounts[0]

dir = os.path.dirname(__file__)
path = os.path.join(dir, 'contracts/FPSBAuction.json')

with open(path, 'r') as f:
    datastore = json.load(f)
abi = datastore["abi"]

def getLatestContract():
    with open(path, 'r') as f:
        datastoreLocal = json.load(f)
    abi = datastoreLocal["abi"]

    networks = datastoreLocal["networks"]
    address_h = ''

    for n in networks:
        address_h = networks[n]['address'];

    address = w3.toChecksumAddress(address_h)
    auction = w3.eth.contract(address=address, abi=abi)

    return auction;
