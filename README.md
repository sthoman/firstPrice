# firstPrice
first price sealed bid auctions on the ethereum blockchain

see research.txt for notes

requirements,

ganache-cli or other RPC node of choice, running on localhost port 8545 for debugging
python v3.7
solc v0.4.24

specific Solidity version installed globally via HomeBrew,

brew unlink solidity
brew install https://raw.githubusercontent.com/ethereum/homebrew-ethereum/9599ce8371d9de039988f89ed577460e58a0f56a/solidity.rb

For truffle deployments,

npm install
npm run compile
npm run deploy

For the middleware, this npm command is dependent on python and starts the middleware,

npm run middleware

the middleware is a python flask server, requires venv and solc v0.4.24

see /middleware/app/__init__.py for the flask routes which utilize the ECRecover scheme

must run truffle deployment before starting middleware
