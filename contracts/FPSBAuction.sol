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
import "@0x/contracts-utils/contracts/utils/Ownable/Ownable.sol";
import "@0x/contracts-tokens/contracts/tokens/ERC721Token/IERC721Token.sol";
import "@0x/contracts-tokens/contracts/tokens/ERC20Token/IERC20Token.sol";
import "./ECRecover.sol";

// A basic prototype FPSBAuction contract implemented as a 0x extension
// contract.
contract FPSBAuction is
  SafeMath, ECRecover, Ownable
{
    using LibBytes for bytes;

    struct Auction {
        uint256 beginCommitTimeSeconds;
        uint256 beginRevealTimeSeconds;
        uint256 currentTimeSeconds;
        uint256 reservePrice;
        uint256 commitCount;
        uint256 revealCount;
        uint256 highestBid;
        address highestBidder;
    }

    //
    address internal WINNER;

    // solhint-disable var-name-mixedcase
    IExchange internal EXCHANGE;

    //
    //constructor(address _exchange)
    constructor()
        public
    {
        EXCHANGE = IExchange(address(0)); ////TODO temporary workaround
    }

    /// @dev The owner of this contract is analogous to the auctioneer, who is responsible for
    //       opening each sealed bid submitted as part of the commit-reveal scheme. Determine
    //       the highest bid off chain but submit it here
    /// @param winner The address of the auction winner
  //  function completeAuction() public onlyOwner() {
  //    WINNER = winner;
  //  }

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
        Auction memory auctionDetails = getAuctionDetails(sellOrder);

        // Ensure the auction has entered reveal phase
        require(
            auctionDetails.currentTimeSeconds >= auctionDetails.beginRevealTimeSeconds,
              "AUCTION_NOT_STARTED"
        );
        // Validate the buyer amount is greater than the reserve price
        require(
            buyOrder.makerAssetAmount >= auctionDetails.reservePrice,
              "INVALID_AMOUNT"
        );
        // Finally, validate that this is the highest bid
        require(
            getBuyerAddress(buyOrder, buySignature) == WINNER,
              "INVALID_WINNER"
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
    /// @return Bid
    function getBuyerAddress(LibOrder.Order memory order, bytes memory buySignature)
        public pure
        returns (address)
    {
        uint256 makerAssetDataLength = order.makerAssetData.length;
        // It is unknown the encoded data of makerAssetData, we assume the last 64 bytes
        // are the Bidder Details encoding of the bidders' salt.
        require(
            makerAssetDataLength >= 100,
            "INVALID_ASSET_DATA"
        );
        // Get the address of the buy order creator, they should have sent their
        // hashed bid amount along in the makerAssetData section of the order
        bytes32 bid = order.makerAssetData.readBytes32(makerAssetDataLength - 64);
        address buyer = ecr(bid, buySignature);

        return buyer;
    }

    /// @dev Calculates the Auction Details for the given order
    /// @param order The sell order
    /// @return Auction
    function getAuctionDetails(
        LibOrder.Order memory order
    )
        public view
        returns (Auction memory auctionDetails)
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
