/*

  Copyright 2019 Sean Thoman

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

*/
pragma solidity 0.4.24;

import "./ECRecover.sol";

// A basic prototype SealedAuction contract, just parts of a basic commit scheme ensuring
// auction participants are not aware of each others' bids during the commit phase of the
// auction.
//
contract SealedAuction is ECRecover
{
  
  struct BidderDetails {
      uint256 amount;
      uint256 salt;
      bytes32 bid;
      bool revealed;
      bool committed;
  }

  // highest bid
  uint256 commitCount;
  uint256 revealCount;
  uint256 highestBid;
  address highestBidder;

  // bidders
  mapping(address => BidderDetails) public bidders;

  // Add a commitment, also known as a bid in this auction. Each bid
  // is hashed by the bidder before submitting to this function. The
  // hash can be validated during the reveal phase by ecrecover.
  function commit(bytes32 bid, bytes memory signature)
    public
  {
    address senderAddress = ecr(bid, signature);
    require(
          senderAddress != address(0), "INVALID_ECRECOVER"
    );
    require(
          bidders[senderAddress].committed == false, "INVALID_COMMIT_UNIQUENESS"
    );
    bidders[senderAddress] = BidderDetails(0, 0, bid, false, true);
    commitCount++;
  }

  // Reveal the salt used to hash each bid as well as the actual bid
  // amount after the auction is closed. This is analogous to opening
  // a sealed envelope containing each bidders' bid amount. When the
  // auction is over this contract can determine the highest bid.
  function reveal(uint256 amount, string salt, bytes memory signature)
    public
  {
    // Revealing a commitment to a previous bid requires the sender
    // to provide their salt and the actual bid amount.
    bytes32 hashed = keccak256(abi.encodePacked(amount, salt));
    address sender = ecr(hashed, signature);
    require(
        bidders[sender].bid == hashed,
          "INVALID_REVEAL"
    );
    //TODO requires for auction state, also sender amount should not be string ultimately
    bidders[sender].revealed = true;
    bidders[sender].amount = amount;

    if (bidders[sender].amount > highestBid) {
      highestBid = bidders[sender].amount;
      highestBidder = sender;
    }
    revealCount++;
  }
}
