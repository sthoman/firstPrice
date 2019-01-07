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

class BidSchema(Schema):
    bid = fields.String(required=True)
    address = fields.String(required=True)

app = Flask(__name__)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))



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



# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# kafka
commitTopic = 'firstPrice-commit'
revealTopic = 'firstPrice-reveal'

@app.route("/auction/commit", methods=['POST'])
def auctionCommit():

    # TODO don't need to do this every time but this makes testing more convenient with frequent re-deployments
    '''
    address_h = getLatestContractAddress()
    address = w3.toChecksumAddress(address_h)
    auction = w3.eth.contract(address=address, abi=abi)

    bid = int(request.form['bid'])
    salt = request.form['salt']
    hash = w3.soliditySha3(['uint256','string'], [bid, salt])

    print(w3.toHex(hash));

    sig = request.form['signature']

    tx_hash = auction.functions.commit(hash, sig).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    '''

    requestJson = request.get_json()

    producerCommit = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    producerCommit.send(commitTopic, requestJson)
    producerCommit.flush()

    return jsonify({"response": ""}), 200



@app.route("/auction/reveal", methods=['POST'])
def auctionReveal():

    '''
    address_h = getLatestContractAddress()
    address = w3.toChecksumAddress(address_h)
    auction = w3.eth.contract(address=address, abi=abi)

    bid = int(request.form['bid'])
    salt = request.form['salt']
    sig = request.form['signature']

    tx_hash = auction.functions.reveal(bid, salt, sig).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    '''

    requestJson = request.get_json()

    producerReveal = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    producerReveal.send(revealTopic, requestJson)
    producerReveal.flush()

    return jsonify({"response": ""}), 200



@app.route("/auction/getPublicKey", methods=['POST'])
def auctionCommitTest():

    address = w3.toChecksumAddress(request.form['address'])
    auction = w3.eth.contract(
        address=address, abi=abi,
    )

    tx_account = w3.eth.account.create('commit test account now')
    tx_private_key = tx_account.privateKey;
    msg = request.form['bid']
    msgHash = defunct_hash_message(text=msg)

    tx_sig = w3.eth.account.signHash(msgHash, private_key=tx_private_key)
    print(w3.toHex(tx_sig['signature']));

    recovered_address = auction.functions.commit(
        msgHash, tx_sig['signature']
    ).call()

    return jsonify({"address": recovered_address}), 200
