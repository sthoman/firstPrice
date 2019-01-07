/*

  Copyright 2018 ZeroEx Intl.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  Modifications copyright (C) 2019 Sean Thoman
*/

pragma solidity 0.4.24;
pragma experimental ABIEncoderV2;

import "@0x/contracts-interfaces/contracts/protocol/Exchange/IExchange.sol";
import "@0x/contracts-libs/contracts/libs/LibOrder.sol";
import "@0x/contracts-utils/contracts/utils/LibBytes/LibBytes.sol";
import "@0x/contracts-utils/contracts/utils/SafeMath/SafeMath.sol";
import "@0x/contracts-tokens/contracts/tokens/ERC721Token/IERC721Token.sol";
import "@0x/contracts-tokens/contracts/tokens/ERC20Token/IERC20Token.sol";
import "./ECRecover.sol";

// A basic prototype FPSBAuction contract implemented as a 0x extension
// contract.
contract FPSBAuction is
  SafeMath, ECRecover
{
    using LibBytes for bytes;

    struct AuctionDetails {
        uint256 beginCommitTimeSeconds;
        uint256 beginRevealTimeSeconds;
        uint256 currentTimeSeconds;
        uint256 reservePrice;
    }

    struct BidderDetails {
        uint256 amount;
        uint256 salt;
        bytes32 bid;
        bool revealed;
        bool committed;
    }

    // solhint-disable var-name-mixedcase
    IExchange internal EXCHANGE;

    // highest bid
    uint256 commitCount;
    uint256 revealCount;
    uint256 highestBid;
    address highestBidder;

    // bidders
    mapping(address => BidderDetails) public bidders;

    //
    //constructor(address _exchange)
    constructor()
        public
    {
        EXCHANGE = IExchange(address(0)); ////TODO temporary workaround
    }

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

    /// @dev Matches the buy and sell orders at an amount given the rules of the auction
    /// @param buyOrder The Buyers' order aka 0x order representation of a previous bid commitment
    /// @param sellOrder The Seller's order. This order is for the reserve price.
    /// @param buySignature Proof that order was created by the buyer.
    /// @param sellSignature Proof that order was created by the seller.
    /// @return matchedFillResults amounts filled and fees paid by maker and taker of matched orders.
    function matchOrders(
        LibOrder.Order memory buyOrder,
        LibOrder.Order memory sellOrder,
        bytes memory buySignature,
        bytes memory sellSignature
    )
        public
        returns (LibFillResults.MatchedFillResults memory matchedFillResults)
    {
        //
        AuctionDetails memory auctionDetails = getAuctionDetails(sellOrder);
        BidderDetails memory bidderDetails = getBidderDetails(buyOrder);

        // Ensure the auction has started
        require(
            auctionDetails.currentTimeSeconds >= auctionDetails.beginRevealTimeSeconds,
            "AUCTION_NOT_STARTED"
        );
        // required??
        //require(
        //    sellOrder.expirationTimeSeconds > auctionDetails.currentTimeSeconds,
        //    "AUCTION_EXPIRED"
        //);
        // Validate the buyer amount is greater than the reserve price
        require(
            buyOrder.makerAssetAmount >= auctionDetails.reservePrice,
            "INVALID_AMOUNT"
        );
        // Validate that this order came from the bidder that committed, which also validates the bidder has revealed
        require(
            bidders[msg.sender].bid == keccak256(abi.encodePacked(buyOrder.makerAssetAmount, bidderDetails.salt)),
            "INVALID_BIDDER"
        );
        // Ensure all reveals are in
        require(
            commitCount == revealCount,
            "INVALID_REVEAL_PHASE"
        );
        // Finally, validate that this is the highest bid
        require(
            msg.sender == highestBidder,
            "INVALID_BID_AMOUNT"
        );

        // Match orders, maximally filling `buyOrder`
        matchedFillResults = EXCHANGE.matchOrders(
            buyOrder,
            sellOrder,
            buySignature,
            sellSignature
        );

        ////TODO what to do here (transfer NFT?)

        return matchedFillResults;
    }

    /// @dev Calculates the Auction Details for the given order
    /// @param order The sell order
    /// @return AuctionDetails
    function getBidderDetails(
        LibOrder.Order memory order
    )
        public pure
        returns (BidderDetails memory bidderDetails)
    {
        uint256 makerAssetDataLength = order.makerAssetData.length;
        // It is unknown the encoded data of makerAssetData, we assume the last 64 bytes
        // are the Bidder Details encoding of the bidders' salt.
        require(
            makerAssetDataLength >= 100,
            "INVALID_ASSET_DATA"
        );
        bidderDetails.salt = order.makerAssetData.readUint256(makerAssetDataLength - 64);

        return bidderDetails;
    }

    /// @dev Calculates the Auction Details for the given order
    /// @param order The sell order
    /// @return AuctionDetails
    function getAuctionDetails(
        LibOrder.Order memory order
    )
        public view
        returns (AuctionDetails memory auctionDetails)
    {
        uint256 makerAssetDataLength = order.makerAssetData.length;
        require(
            makerAssetDataLength >= 100,
            "INVALID_ASSET_DATA"
        );
        uint256 auctionBeginCommitTimeSeconds = order.makerAssetData.readUint256(makerAssetDataLength - 64);
        uint256 auctionBeginRevealTimeSeconds = order.makerAssetData.readUint256(makerAssetDataLength - 32);

        // Ensure the auction reveal time is greater than commit time
        require(
            auctionBeginRevealTimeSeconds > auctionBeginCommitTimeSeconds,
            "REVEAL_TIME_MUST_BE_GREATER"
        );

        // Ensure the auction has a reserve price
        uint256 reservePrice = order.takerAssetAmount;

        // solhint-disable-next-line not-rely-on-time
        uint256 timestamp = block.timestamp;
        auctionDetails.beginCommitTimeSeconds = auctionBeginCommitTimeSeconds;
        auctionDetails.beginRevealTimeSeconds = auctionBeginRevealTimeSeconds;
        auctionDetails.currentTimeSeconds = timestamp;
        auctionDetails.reservePrice = reservePrice;

        return auctionDetails;
    }
}
