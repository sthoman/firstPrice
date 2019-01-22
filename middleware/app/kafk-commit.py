import json
import sha3
import os
from kafka import KafkaConsumer
from web3 import Web3
from eth_account.messages import defunct_hash_message
from sha3 import keccak_256
from eth import getLatestAuctionContract, getLatestCommitContract


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

delegate_account = w3.eth.account.create('the quick brown fox jumps over the lazy programmer')
delegate_private_key = delegate_account.privateKey

w3.eth.defaultAccount = w3.eth.accounts[0]

#w3.personal.unlockAccount(account,"password",15000); // unlock for a long time

consumerCommitTopic = KafkaConsumer(
            'firstPrice-commit',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
        )
''' This is the main entry point for all bid commitments, which are hashed and signed by
    both the end user (bidder) and the account which sends bids to the auction contract
    on behalf of the bidder. The bidders' signature should come from the client so that
    this service doesn't need to hold the private key. A secret, random salt should also
    be sent from the client
'''
def consumerCommit(kafkMessage):
    auction = getLatestAuctionContract()
    commitcontract = getLatestCommitContract()

    bid = int(kafkMessage.value['bid'])
    salt = kafkMessage.value['salt']
    hash = w3.soliditySha3(['uint256','string'], [bid, salt])
    addr = auction.address

    sig = w3.eth.account.signHash(hash, private_key=delegate_private_key)
    sign = sig['signature']
    print(sign)
    print(hash)
    print(commitcontract.address)

    tx_hash = commitcontract.functions.commit(hash, sign, addr).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print('tx_receipt=')
    print(tx_receipt)

# TODO need a solution to not re-consume the same messages, or also
# on chain could add validation
for msg in consumerCommitTopic:
    #try:
        consumerCommit(msg)
    #except:
    #    print('except')
