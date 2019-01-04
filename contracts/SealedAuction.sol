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

// A basic prototype SealedAuction contract, just parts of a basic commit scheme ensuring
// auction participants are not aware of each others' bids during the commit phase of the
// auction.
//
contract SealedAuction
{
    struct AuctionDetails {
        uint256 beginTimeSeconds;
        uint256 endTimeSeconds;
        uint256 beginRevealTimeSeconds;
        uint256 currentTimeSeconds;
        uint256 reservePrice;
    }

    struct BidderDetails {
        uint256 salt;
        bytes32 bid;
        uint256 amount;
        bool revealed;
    }

    // highest bid
    uint256 commitCount;
    uint256 revealCount;
    uint256 highestBid;
    address highestBidder;

    // bidders
    mapping(address => BidderDetails) public bidders;

    //
    constructor() public { }

    // Add a commitment, also known as a bid in this auction. Each bid
    // is hashed by the bidder before submitting to this function. The
    // hash can later be validated during the reveal phase.
    function addCommit(bytes32 bid)
      public
    {
      require(
            bidders[msg.sender].bid == bid,
            "INVALID_COMMIT_UNIQUENESS"
      );
      bidders[msg.sender] = BidderDetails(0, bid, 0, false);
      commitCount++;
    }

    // Reveal the salt used to hash each bid as well as the actual bid
    // amount after the auction is closed. This is analogous to opening
    // a sealed envelope containing each bidders' bid amount. When the
    // auction is over this contract can determine the highest bid.
    //
    function addReveal(bytes32 salt, uint256 amount)
      public
    {
      // Revealing a commitment to a previous bid requires the sender
      // to provide their salt and the actual bid amount. It should not
      // already be revealed
      require(
          bidders[msg.sender].revealed == true,
            "INVALID_REVEAL_UNIQUENESS"
      );
      require(
          bidders[msg.sender].bid == keccak256(amount, salt),
            "INVALID_REVEAL"
      );
      //TODO requires for auction state
      bidders[msg.sender].revealed = true;
      bidders[msg.sender].amount = amount;
      //
      if (bidders[msg.sender].amount > highestBid) {
        highestBid = bidders[msg.sender].amount;
        highestBidder = msg.sender;
      }
      revealCount++;
    }
}
