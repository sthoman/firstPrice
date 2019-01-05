import json
import web3

from web3 import Web3
from eth_account.messages import defunct_hash_message

hex_message = '0x49e299a55346'
hex_signature = '0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb33e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce1c'

# ecrecover in Solidity expects a prefixed & hashed version of the message
message_hash = defunct_hash_message(hexstr=hex_message)

# Remix / web3.js expect the message hash to be encoded to a hex string
hex_message_hash = Web3.toHex(message_hash)

# ecrecover in Solidity expects the signature to be split into v as a uint8,
#   and r, s as a bytes32
# Remix / web3.js expect r and s to be encoded to hex
sig = Web3.toBytes(hexstr=hex_signature)
v, hex_r, hex_s = Web3.toInt(sig[-1]), Web3.toHex(sig[:32]), Web3.toHex(sig[32:64])

# ecrecover in Solidity takes the arguments in order = (msghash, v, r, s)
ec_recover_args = (hex_message_hash, v, hex_r, hex_s)

# print
print(ec_recover_args)
