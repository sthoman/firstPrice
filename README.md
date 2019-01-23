# firstPrice

First price sealed bid auctions on the ethereum blockchain (WIP).

## Abstract

This project, for Lighthouse Labs' October 2018 blockchain cohort, is primarily an exploration of 
using the Ethereum blockchain to securely compute the winning bid amongst bidders in a sealed auction; 
that is, where participants are not aware of each others' bid amounts until after the auction is over.

## Commitment Scheme 

First price sealed bid auctions are a kind of auction in which n participants are allowed to submit sealed 
bids for some asset within a time frame as long as the bid is above a reserve price for that asset. Bids are 
private and hidden from all the participants. It is analogous to collecting bids in a sealed envelope, and 
waiting until after the auction is over to open each envelope and determine the highest bidder.

The SealedCR contract (standing for, sealed commit reveal) implements a commitment scheme where N bidders
submit a hash of their bid amount during the commitment phase of the auction. The commitment phase of the 
auction has a publicly defined start and end time. Once the commitment phase end time is reached, the auction 
will enter a reveal phase. Participants may call the reveal() function to expose their bid amounts along with
the random salt value they used to hash their bid during the commitment phase. 

If the resultant hashes match, the bid is valid. The contract will track the highest bid as the reveal()
function is called by each participant during the reveal phase. Once all reveals are complete, the highest
bidder can be determined on chain and an order can be signed and filled to complete the transaction.

## State Channel

In this scheme, hashed bids are commitments and cleartext bids reveal the true value of commitments. Instead
of requiring participants to transact with a smart contract, hashed bid commitments could be distributed amongst 
the buyers and sellers throughout the auction. Buyers would sign their commitments using the private key of a 
special account created on their client, which is tied to their master key. 

This type of delegated signing means the user only has to use Metamask once to enter the auction, which calls 
the smart contract to establish which account they will be using to sign their transactions. During the reveal
phase of the auction, if disputes between participants were to arise, any one participant could call the smart
contract to prove their commitment to a certain bid. 

## Why Blockchain?

A blockchain is a perfect medium for recording commitments to some value that may be revealed at a later 
time or state. So if designed correctly, it should be very difficult for auction participants to collude
with each other or otherwise sabotage the auction. At the same time, anyone in the world could adjudicate
on the fairness of the auction if provided with an honest record of those commitments and revealed bids.

Even more importantly, this kind of auction is essentially a game of incomplete information amongst bidders 
with interesting game theoretic properties like Nash equilibria. They may be useful in price discovery for 
difficult to price goods or services. If decentralization will usher in new types of previously unimagined 
digital assets, it seems natural that effective and fair price discovery for both buyers and sellers would 
be a worthy area of research.

## Setup

- Install Python v3.7 
- Install virtualenv (for Python)
- Install pip/pip3 (for Python)
- Install Ganache
- Install Truffle
- Install solc v0.4.24
- Install Vue.js

### Truffle Project

The root level is a Truffle project, to build and deploy to a development node running on 127.0.0.1:8545, run the 
following NPM scripts, after running npm install, 

    "deploy": "./node_modules/.bin/truffle deploy --reset --network bridge"

### Python Flask 

The /middleware folder is a Python flask server project that requires a virtualenv and several Python dependencies
in a few requirements text files. The following NPM scripts will build the environment, and then start it, 

    "venv-build": "venv/bin/pip3 install -r requirements_3_7.txt && venv/bin/pip install -r requirements_2_7.txt",
    "venv": "source middleware/venv/bin/activate",

This command will copy the smart contract metadata into the Python project and then start the flask server, 

    "middleware": "mkdir -p middleware/app/contracts/ && cp -R build/contracts/*.* middleware/app/contracts/ && cd middleware && flask run",
   
