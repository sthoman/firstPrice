import json
import sha3
import os
from kafka import KafkaConsumer
from web3 import Web3
from eth_account.messages import defunct_hash_message
from sha3 import keccak_256



w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.defaultAccount = w3.eth.accounts[0]

dir = os.path.dirname(__file__)
path = os.path.join(dir, 'contracts/FPSBAuction.json')

with open(path, 'r') as f:
    datastore = json.load(f)
abi = datastore["abi"]

def getLatestContractAddress():
    with open(path, 'r') as f:
        datastoreLocal = json.load(f)
    abi = datastoreLocal["abi"]

    networks = datastoreLocal["networks"]
    address_h = ''

    for n in networks:
        address_h = networks[n]['address'];

    return address_h;



consumerCommitTopic = KafkaConsumer(
            'firstPrice-commit',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
        )



def consumerCommit(kafkMessage):
    address_h = getLatestContractAddress()
    address = w3.toChecksumAddress(address_h)
    auction = w3.eth.contract(address=address, abi=abi)

    sig = kafkMessage.value['signature']
    bid = int(kafkMessage.value['bid'])
    salt = kafkMessage.value['salt']
    hash = w3.soliditySha3(['uint256','string'], [bid, salt])

    tx_hash = auction.functions.commit(hash, sig).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)




# TODO need a solution to not re-consume the same messages, or also
# on chain could add validation
for msg in consumerCommitTopic:
    consumerCommit(msg)
