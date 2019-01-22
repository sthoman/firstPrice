import json
import sha3
import os
from kafka import KafkaConsumer, KafkaProducer
from web3 import Web3
from eth_account.messages import defunct_hash_message
from sha3 import keccak_256
from eth import getLatestAuctionContract, getLatestCommitContract


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

delegate_account = w3.eth.account.create('the quick brown fox jumps over the lazy programmer')
delegate_private_key = tx_account.privateKey

w3.eth.defaultAccount = delegate_account


consumerRevealTopic = KafkaConsumer(
            'firstPrice-reveal',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
        )

# TODO consider encrypted reveals?
def consumerReveal(kafkMessage):
    auction = getLatestAuctionContract()
    commitContract = getLatestCommitContract()
    sig = kafkMessage.value['signature']
    bid = int(kafkMessage.value['bid'])
    salt = kafkMessage.value['salt']
    #addr = kafkMessage.value['addr'] # TODO the address of the auction
    addr = auction.address

    #tx_hash = commitContract.functions.reveal(bid, salt, sig, addr).transact()
    tx_hash = commitContract.functions.reveal(bid, salt).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)

# TODO need a solution to not re-consume the same messages, or also
# on chain could add validation?
for msg in consumerRevealTopic:
    consumerReveal(msg)
