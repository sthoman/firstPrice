import json
import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

dir = os.path.dirname(__file__)
path = os.path.join(dir, 'contracts/FPSBAuction.json')
path_cr = os.path.join(dir, 'contracts/SealedCR.json')

w3.eth.defaultAccount = w3.eth.accounts[0]

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
    with open(path_cr, 'r') as g:
        datastoreLocalCr = json.load(g)
    abi_cr = datastoreLocalCr["abi"]

    networks_cr = datastoreLocalCr["networks"]
    address_h = '0x4f56e0f93753b92da241d0a1eca44630b1cb16dd'

    for n in networks_cr:
        address_h = networks_cr[n]['address'];

    address_cr = w3.toChecksumAddress('0xbed379c43df8b0e9c1c7b1cbc877aab4c35b32e5')
    print('address_cr=');
    print(address_cr);
    commitContract = w3.eth.contract(address=address_cr, abi=abi_cr)

    return commitContract;
