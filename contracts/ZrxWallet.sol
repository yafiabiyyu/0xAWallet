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

    event DepositToken(address token, address sender, uint256 amount);
    event WithdrawToken(address token, address sender, uint256 amount);
    event TransferToken(
        address token,
        address sender,
        address to,
        uint256 amount
    );

    modifier checkEtherBalance(uint256 amount) {
        require(address(this).balance >= amount, "You don't have enough ether");
        _;
    }

    modifier checkAllowance(
        address token,
        address sender,
        address spender,
        uint256 amount
    ) {
        require(
            IERC20(token).allowance(sender, spender) >= amount,
            "You don't have enough allowance"
        );
        _;
    }

    modifier checkTokenBalance(address token, uint256 amount) {
        require(
            IERC20(token).balanceOf(address(this)) >= amount,
            "You don't have enough tokens"
        );
        _;
    }

    function depositEther() external payable onlyOwner {
        require(msg.value > 0, "You must send ether to deposit");
        emit DepositEther(msg.sender, msg.value);
    }

    function withdrawEther(uint256 amount)
        external
        checkEtherBalance(amount)
        onlyOwner
    {
        require(amount > 0, "Amount must be greater than 0");
        (bool sent, ) = msg.sender.call{value: amount}("");
        require(sent, "Ether transfer failed");
    }

    function transferEther(address payable to, uint256 amount)
        external
        payable
        checkEtherBalance(amount)
        onlyOwner
    {
        require(amount > 0, "Amount must be greater than 0");
        require(to != address(0), "You can't send ether to the null address");
        (bool sent, ) = to.call{value: amount}("");
        require(sent, "Ether transfer failed");
        emit TransferEther(msg.sender, to, amount);
    }

    function getTokenBalance(address token)
        external
        view
        onlyOwner
        returns (uint256)
    {
        return IERC20(token).balanceOf(address(this));
    }

    function depositToken(address token, uint256 amount)
        external
        checkAllowance(token, msg.sender, address(this), amount)
        onlyOwner
    {
        require(amount > 0, "Amount must be greater than 0");
        require(token != address(0), "Token cannot be the null address");
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
        emit DepositToken(token, msg.sender, amount);
    }

    function withdrawToken(address token, uint256 amount)
        external
        checkTokenBalance(token, amount)
        onlyOwner
    {
        require(amount > 0, "Amount must be greater than 0");
        require(token != address(0), "Token cannot be the null address");
        IERC20(token).safeTransfer(msg.sender, amount);
        emit WithdrawToken(token, msg.sender, amount);
    }

    function transferToken(
        address token,
        address to,
        uint256 amount
    ) external checkTokenBalance(token, amount) onlyOwner {
        require(token != address(0), "Token cannot be the null address");
        require(to != address(0), "You can't send ether to the null address");
        require(amount > 0, "Amount must be greater than 0");
        IERC20(token).safeTransfer(to, amount);
        emit TransferToken(token, address(this), to, amount);
    }
}
