import json
import sha3
import os
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3
from eth_account.messages import defunct_hash_message
from sha3 import keccak_256
from kafka import KafkaProducer
from kafka.errors import KafkaError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# kafka
commitTopic = 'firstPrice-commit'
revealTopic = 'firstPrice-reveal'

@app.route("/auction/abi", methods=['GET'])
def getContractAbi():
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'contracts/SealedCR.json')

    with open(path, 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]

    return jsonify({"response": abi}), 200

@app.route("/auction/commit", methods=['POST'])
def auctionCommit():
    requestJson = request.get_json()
    producerCommit = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    producerCommit.send(commitTopic, requestJson)
    producerCommit.flush()

    return jsonify({"response": ""}), 200

@app.route("/auction/reveal", methods=['POST'])
def auctionReveal():
    requestJson = request.get_json()
    producerReveal = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    producerReveal.send(revealTopic, requestJson)
    producerReveal.flush()

    return jsonify({"response": ""}), 200


'''
@app.route("/auction/init", methods=['POST'])
def auctionCommitTest():

    address = w3.toChecksumAddress(request.form['address'])
    auction = w3.eth.contract(
        address=address, abi=abi,
    )

    delegate_account = w3.eth.account.create('the quick brown fox jumps over the lazy programmer')
    delegate_private_key = tx_account.privateKey;

    msg = request.form['bid']
    msgHash = defunct_hash_message(text=msg)

    delegate_sig = w3.eth.account.signHash(msgHash, private_key=delegate_private_key)

    print(w3.toHex(tx_sig['signature']));

    recovered_address = auction.functions.commit(
        msgHash, tx_sig['signature']
    ).call()

    return jsonify({"address": recovered_address}), 200
'''
