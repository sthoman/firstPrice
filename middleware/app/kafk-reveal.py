import json
import sha3
import os
from kafka import KafkaConsumer
from web3 import Web3
from eth_account.messages import defunct_hash_message
from sha3 import keccak_256
from eth import getLatestContract


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


consumerRevealTopic = KafkaConsumer(
            'firstPrice-reveal',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
        )

def consumerReveal(kafkMessage):
    auction = getLatestContract()
    sig = kafkMessage.value['signature']
    bid = int(kafkMessage.value['bid'])
    salt = kafkMessage.value['salt']

    tx_hash = auction.functions.reveal(bid, salt, sig).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)

# TODO need a solution to not re-consume the same messages, or also
# on chain could add validation?
for msg in consumerRevealTopic:
    consumerReveal(msg)
