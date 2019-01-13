import json
import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

dir = os.path.dirname(__file__)
path = os.path.join(dir, 'contracts/FPSBAuction.json')
path_cr = os.path.join(dir, 'contracts/SealedAuction.json')

with open(path, 'r') as f:
    datastore = json.load(f)
abi = datastore["abi"]

''' Off chain mechanism to determine the highest bidder,
    somewhat as an oracle might, and then attest to that
    result on chain.
'''
def getHighestBidderForAuction():
    return

''' A temporary build solution get get the latest contract
    from the network
'''
def getLatestAuctionContract():
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

''' A temporary build solution get get the latest contract
    from the network
'''
def getLatestCommitContract():
    with open(path_cr, 'r') as f:
        datastoreLocal = json.load(f)
    abi = datastoreLocal["abi"]

    networks = datastoreLocal["networks"]
    address_h = ''

    for n in networks:
        address_h = networks[n]['address'];

    address = w3.toChecksumAddress(address_h)
    commitContract = w3.eth.contract(address=address, abi=abi)

    return commitContract;
