import json
import sha3
import os
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3
from eth_account.messages import defunct_hash_message
from sha3 import keccak_256

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



@app.route("/auction/commit", methods=['POST'])
def auctionCommit():

    address = w3.toChecksumAddress('0x0a45e1ac0f4d00adf66b292da76ae23f3c0e06cc') #TODO will not be hardcoded
    auction = w3.eth.contract(address=address, abi=abi)

    salt = "dont_touch_my_salt"
    bid = "1"
    bidBytes = w3.toBytes(text=bid);
    saltBytes = w3.toBytes(text=salt);

    msgHash = w3.soliditySha3(['bytes32','bytes32'], [bidBytes, saltBytes]);

    print(w3.toHex(msgHash))
    sig = request.form['signature']

    ecrec = auction.functions.commit(msgHash, sig).call()

    return jsonify({"response": ""}), 200



@app.route("/auction/reveal", methods=['POST'])
def auctionReveal():

    address = w3.toChecksumAddress('0x0a45e1ac0f4d00adf66b292da76ae23f3c0e06cc')
    auction = w3.eth.contract(address=address, abi=abi)

    salt = "dont_touch_my_salt"
    bid = "1"
    bidBytes = w3.toBytes(text=bid);
    saltBytes = w3.toBytes(text=salt);

    sig = request.form['signature']

    ecrec = auction.functions.reveal(saltBytes, bidBytes, sig).call()
    ecrecHex = w3.toHex(ecrec)

    return jsonify({"response": ""}), 200



@app.route("/auction/commit-test", methods=['POST'])
def auctionCommitTest():

    w3.eth.defaultAccount = w3.eth.accounts[1]

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
