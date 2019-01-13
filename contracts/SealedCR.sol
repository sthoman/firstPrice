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

import "@0x/contracts-utils/contracts/utils/LibBytes/LibBytes.sol";
import "@0x/contracts-utils/contracts/utils/Ownable/Ownable.sol";
import "./ECRecover.sol";

// Sealed commit reveal scheme for sealed bid auctions. This contract
// is solely responsible for receiving hashed bid commitments during
// the commit phase of the auction, and receiving the revealed amount
// during the reveal phase. It does not determine the highest bidder
// but anyone should be able to examine the results of this contract
// to contest the winner.
contract SealedCR is ECRecover, Ownable
{
    using LibBytes for bytes;

    //
    struct Bid {
        address auctionContract;  // the auction contract this bid is for
        address senderAddr;       // the address of the bid sender
        address revealAddr;       // the address of the bid revealer, should match
        bytes32 revealHash;       // the hash from the reveal operation
        uint256 revealAmount;     // the clear bid value
        bytes commitSignature;    // signature of the bid sender
    }

    // mapping of commit hash to bid object
    mapping(bytes32 => Bid) public bids;

    // Add a commitment, also known as a bid in this auction. Each bid
    // is hashed by the bidder before submitting to this function. The
    // hash can be validated during a challenge by ecrecover.
    //
    function commit(bytes32 commitHash, bytes memory signature, address auctionContract)
      public
      //onlyOwner()
    {
      address senderAddress = ecr(commitHash, signature);
      require(
            senderAddress != address(0),
              "ECRECOVER_FAILED"
      );
      bids[commitHash] = Bid(auctionContract, senderAddress, address(0), 0, 0, signature);
    }

    // Reveal the salt used to hash each bid as well as the actual bid
    // amount after the auction is closed. This is analogous to opening
    // a sealed envelope containing each bidders' bid amount.
    function reveal(uint256 revealAmount, string salt)
      public
      //onlyOwner()
    {
      // Revealing a commitment to a previous bid requires the sender
      // to provide their random salt and the actual bid amount.
      bytes32 revealHash = keccak256(abi.encodePacked(revealAmount, salt));
      require(
          bids[revealHash].senderAddr != address(0),
            "REVEAL_HASH_FAILED"
      );
      bids[revealHash].revealHash = revealHash;
      bids[revealHash].revealAmount = revealAmount;
    }

    // Since reveal() gave this contract the true bid amounts, now any
    // off chain process can compute the highest bid without incurring
    // any gas fees. Whomever computes the highest bid shall sign their
    // decision. Anyone can challenge the decision using this function
    // if it turns out the bid commitment address DOES NOT match the
    // revealers address.
    //
    // This is purposely the only function that is not marked onlyOwner()
    //
    function challenge(uint256 revealAmount, string salt, bytes memory signature)
      public
    {
  //    bytes32 commitSignature = signature;
      bytes32 revealHash = keccak256(abi.encodePacked(revealAmount, salt));
      address revealAddress = ecr(revealHash, signature);
  //    require(
  //        bids[revealHash].commitSignature == commitSignature,
  //          "CHALLENGE_FAILED_BAD_SIGNATURE"
  //    );
      require(
          bids[revealHash].senderAddr != revealAddress,
            "CHALLENGE_FAILED"
      );
      bids[revealHash].revealAddr = revealAddress;
      // CONSEQUENCE?
    }
}
