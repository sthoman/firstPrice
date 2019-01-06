import json
import os
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3
from eth_account.messages import defunct_hash_message

class BidSchema(Schema):
    bid = fields.String(required=True)
    address = fields.String(required=True)


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


app = Flask(__name__)


@app.route("/auction/commit-test", methods=['POST'])
def transaction():

    w3.eth.defaultAccount = w3.eth.accounts[1]

    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'contracts/FPSBAuction.json')

    with open(path, 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]

    address = w3.toChecksumAddress(request.form['address'])
    auction = w3.eth.contract(
        address=address, abi=abi,
    )

    tx_account = w3.eth.account.create('commit test account now')
    tx_private_key = tx_account.privateKey;
    msg = request.form['bid']
    msgHash = defunct_hash_message(text=msg)

    tx_sig = w3.eth.account.signHash(msgHash, private_key=tx_private_key)

    recovered_address = auction.functions.commit(
        msgHash, tx_sig['signature']
    ).call()

    return jsonify({"address": recovered_address}), 200
