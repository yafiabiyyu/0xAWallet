// SPDX-License-Identifier: MIT
pragma solidity 0.8.1;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract ZrxWallet is Ownable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;

    event DepositEther(address sender, uint256 amount);
    event WithdrawEther(address sender, uint256 amount);
    event TransferEther(address sender, address to, uint256 amount);

    function depositEther() external payable onlyOwner {
        require(msg.value > 0, "You must send ether to deposit");
        emit DepositEther(msg.sender, msg.value);
    }

    function withdrawEther(uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than 0");
        require(address(this).balance >= amount, "You don't have enough ether");
        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Ether transfer failed");
    }

    function transferEther(address payable to, uint256 amount)
        external
        payable
        onlyOwner
    {
        require(amount > 0, "Amount must be greater than 0");
        require(address(this).balance >= amount, "You don't have enough ether");
        require(to != address(0), "You can't send ether to the null address");
        (bool sent, ) = to.call{value: amount}("");
        require(sent, "Ether transfer failed");
        emit TransferEther(msg.sender, to, amount);
    }
}
