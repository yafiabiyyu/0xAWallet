// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract ZrxAWallet is Ownable {
    uint256 claimPeriod;
    mapping(address => uint256) private balance;

    event newClaimPeriode(uint256);
    event EtherDeposit(address _sender, uint256 _etherAmount);

    constructor(uint256 _claimPeriod) {
        claimPeriod = block.timestamp + (_claimPeriod * 1 days);
    }

    modifier onlyClaimPeriod() {
        require(block.timestamp > claimPeriod);
        _;
    }

    function updateClaimPeriod(uint256 _newClaimPeriod) public onlyOwner {
        require(_newClaimPeriod > 0);
        uint256 period = _newClaimPeriod * 1 days;
        claimPeriod = block.timestamp + period;
        emit newClaimPeriode(period);
    }

    function depositEther() public payable onlyOwner {
        require(msg.value > 0);
        balance[msg.sender] += msg.value;
        emit EtherDeposit(msg.sender, msg.value);
    }

    function withdrawEther(uint256 _etherAmount) public onlyOwner {
        require(_etherAmount > 0);
        require(balance[msg.sender] >= _etherAmount);
        balance[msg.sender] -= _etherAmount;
        (bool sent, ) = payable(msg.sender).call{value: _etherAmount}("");
        require(sent, "Ether transfer failed");
    }
}
