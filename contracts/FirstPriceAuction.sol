pragma solidity 0.4.24;
pragma experimental ABIEncoderV2;

import "@0x/contracts-tokens/contracts/tokens/ERC721Token/IERC721Token.sol";
import "@0x/contracts-tokens/contracts/tokens/ERC20Token/IERC20Token.sol";

// A basic prototype FirstPriceAuction contract, just parts of commit scheme
contract FirstPriceAuction
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

    /// Add a commitment, also known as a bid in this auction. Each bid
    /// is hashed by the bidder before submitting to this function. The
    /// hash can later be validated during the reveal phase.
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

    /// Reveal the salt used to hash each bid as well as the actual bid
    /// amount after the auction is closed. This is analogous to opening
    /// a sealed envelope containing each bidders' bid amount. When the
    /// auction is over this contract can determine the highest bid.
    ///
    function addReveal(bytes32 salt, uint256 amount) {
      /// Revealing a commitment to a previous bid requires the sender
      /// to provide their salt and the actual bid amount. It should not
      /// already be revealed
      require(
          bidders[msg.sender].revealed == true,
            "INVALID_REVEAL_UNIQUENESS"
      );
      require(
          bidders[msg.sender].bid == keccak256(amount, salt),
            "INVALID_REVEAL"
      );
      ////TODO requires for auction state
      bidders[msg.sender].revealed = true;
      bidders[msg.sender].amount = amount;
      ////
      if (bidders[msg.sender].amount > highestBid) {
        highestBid = bidders[msg.sender].amount;
        highestBidder = msg.sender;
      }
      revealCount++;
    }
}
