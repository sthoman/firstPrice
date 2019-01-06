const FPSBAuction = artifacts.require("./FPSBAuction.sol");

contract('FPSBAuction Contract Tests', accounts => {

  hexSignature = '0x2eb1c04a8517937124c2580f263738e34d893bd4f9da48f66220f22db3f9c0a5558a9eff3e37d06e1509c22c3a5ac02c55445280620e9c1c43c2e6c2aae56fd51c';
  hexMessageHash = '0x50b2c43fd39106bafbba0da34fc430e1f91e3c96ea2acee2bc34119f92b37750';

  it('should correctly use ecrecover for a bid commitment, FPSBAuction', async () => {
    fpsbAuction = await FPSBAuction.deployed();
    fpsbAuctionAddr = fpsbAuction.address;
    fpsbAuctionCommit = await fpsbAuction.commit.call(hexMessageHash, hexSignature);
    assert(fpsbAuctionCommit, 'Correctly used ecrecover for a bid commitment')
  });

});
