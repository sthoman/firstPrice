from app import app
from web3 import Web3
from flask import render_template

@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')
