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

global commitsDeployed
global commitsContractAddress
global commitsContractAb

#
commitsDeployed = False
commitsContractAddress = ''
commitsContractAbi = ''
commitTopic = 'firstPrice-commit'
revealTopic = 'firstPrice-reveal'

#
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.defaultAccount = w3.eth.accounts[0]


# current implementation - no args in constructor
def deployContractAtPath(path):
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, path)
    data = dict()

    with open(path, 'r') as f:
        datastore = json.load(f)

    fpsb = w3.eth.contract(abi=datastore['abi'], bytecode=datastore['bytecode'])
    tx_hash = fpsb.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    data['receipt'] = tx_receipt
    data['abi'] = datastore['abi']
    return data


@app.route("/commits/create", methods=['PUT'])
def deployCommitContractAbi():
    res = deployContractAtPath('contracts/SealedCR.json')
    commitsContractAddress = res['receipt'].contractAddress
    commitsDeployed = True
    commitsContractAbi = res['abi']
    return jsonify({ "address": commitsContractAddress, "abi": commitsContractAbi }), 200

# Only creates the commit contract if it doesn't already exist
@app.route("/commits/register", methods=['POST'])
def registerCommit():
    global commitsDeployed
    global commitsContractAddress
    global commitsContractAbi
    if commitsDeployed == False:
        res = deployContractAtPath('contracts/SealedCR.json')
        commitsContractAddress = res['receipt'].contractAddress
        commitsDeployed = True
        commitsContractAbi = res['abi']
    return jsonify({ "address": commitsContractAddress, "abi": commitsContractAbi }), 200

@app.route("/commits/abi", methods=['GET'])
def getContractAbi():
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'contracts/SealedCR.json')

    with open(path, 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]

    return jsonify({"response": abi}), 200

@app.route("/commits/bid", methods=['PUT'])
def submitBidCommitment():
    global commitsContractAddress
    global commitsContractAbi
    json = request.get_json()

    commits = w3.eth.contract(address=commitsContractAddress, abi=commitsContractAbi)

    bid = json['bid'].lstrip('0x')
    sig = json['sig'].lstrip('0x')
    addr = json['auction_address']

    bid = w3.toBytes(hexstr=bid)
    sig = w3.toBytes(hexstr=sig)

    tx_hash = commits.functions.commit(bid, sig, addr).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({"response": tx_receipt}), 200



@app.route("/auction/create", methods=['PUT'])
def deployContractAbi():
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'contracts/FPSBAuction.json')

    with open(path, 'r') as f:
        datastore = json.load(f)

    fpsb = w3.eth.contract(abi=datastore['abi'], bytecode=datastore['bytecode'])
    tx_hash = fpsb.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({ "address": tx_receipt.contractAddress }), 200

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
