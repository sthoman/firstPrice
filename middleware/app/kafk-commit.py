import json
import sha3
import os
from kafka import KafkaConsumer
from web3 import Web3
from eth_account.messages import defunct_hash_message
from sha3 import keccak_256
from eth import getLatestContract


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

delegate_account = w3.eth.account.create('the quick brown fox jumps over the lazy programmer')
delegate_private_key = tx_account.privateKey;

w3.eth.defaultAccount = delegate_account


consumerCommitTopic = KafkaConsumer(
            'firstPrice-commit',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
        )
''' This is the main entry point for all bid commitments, which are hashed and signed by
    both the end user (bidder) and the account which sends bids to the auction contract
    on behalf of the bidder. The bidders' signature should come from the client so that
    this service doesn't need to hold the private key. A secret, random salt should also
    be sent from the client
'''
def consumerCommit(kafkMessage):
    auction = getLatestContract()
    sig = kafkMessage.value['signature']
    bid = int(kafkMessage.value['bid'])
    salt = kafkMessage.value['salt']
    hash = w3.soliditySha3(['uint256','string'], [bid, salt])

    delegate_sig = w3.eth.account.signHash(hash, private_key=delegate_private_key)

    tx_hash = auction.functions.commit(hash, sig).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)

# TODO need a solution to not re-consume the same messages, or also
# on chain could add validation
for msg in consumerCommitTopic:
    consumerCommit(msg)
