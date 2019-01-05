from flask import Flask
from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {} # dict to track active rooms

from app import routes

@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    emit('join_room', {'room': 1})

if __name__ == '__main__':
    socketio.run(app, debug=True)

## decent cult Github

## generating the past is blockchain, a past-generation machine

# non-fungible token to represent physical assets, e.g. antiques ERC721
# non-fungible token to represent digital upload - feasible project

# content creation, generally

# legacy management

# look up Skinny CREATE2

# the basic idea of all this is that users act as if they are on the blockchain
# even off-chain, and if disputes arise then only on-chain solutions needed
