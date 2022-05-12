// SPDX-License-Identifier: MIT
pragma solidity 0.8.1;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import "@openzeppelin/contracts/utils/math/SafeMath.sol";

import "../interfaces/ILendingPool.sol";

import "../interfaces/ILendingPoolAddressesProvider.sol";

import "../interfaces/IWETHGateway.sol";

contract ZrxWallet is Ownable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;

    ILendingPoolAddressesProvider poolProvider =
        ILendingPoolAddressesProvider(
            0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5
        );
    ILendingPool pool =
        ILendingPool(0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9);
    IWETHGateway wethGateway =
        IWETHGateway(0xcc9a0B7c43DC2a5F023Bb9b738E45B0Ef6B06E04);
    IERC20 aWeth = IERC20(0x030bA81f1c18d280636F32af80b9AAd02Cf0854e);

    mapping(address => address) private tokenToaToken;

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

    event LockEther(address sender, uint256 amount);
    event UnlockEther(address sender, uint256 amount);
    event LockToken(address tokenAddress, address sender, uint256 amount);
    event UnlockToken(address tokenAddress, address sender, uint256 amount);

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

    modifier onlyWethGateway() {
        require(msg.sender == address(wethGateway), "Only WETH gateway");
        _;
    }

    constructor(address[] memory tokens, address[] memory atokens) {
        require(
            tokens.length == atokens.length,
            "Tokens and addresses must be equal"
        );
        for (uint256 i = 0; i < tokens.length; i++) {
            tokenToaToken[tokens[i]] = atokens[i];
        }
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

    function lockEther(uint256 amount)
        external
        onlyOwner
        checkEtherBalance(amount)
    {
        require(amount > 0, "Amount must be greater than 0");
        wethGateway.depositETH{value: amount}(address(pool), address(this), 0);
        emit LockEther(address(this), amount);
    }

    function unlockEther(uint256 amount)
        external
        checkTokenBalance(address(aWeth), amount)
        onlyOwner
    {
        require(amount > 0, "Amount must be greater than 0");
        aWeth.approve(address(wethGateway), amount);
        wethGateway.withdrawETH(address(pool), amount, address(this));
        emit UnlockEther(address(this), amount);
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

    function lockToken(address token, uint256 amount)
        external
        checkTokenBalance(token, amount)
        onlyOwner
    {
        require(token != address(0), "Token cannot be the null address");
        require(amount > 0, "Amount must be greater than 0");
        IERC20(token).approve(address(pool), amount);
        pool.deposit(token, amount, address(this), 0);
        emit LockToken(token, address(this), amount);
    }

    function unlockToken(address token, uint256 amount) external onlyOwner {
        require(token != address(0), "Token cannot be the null address");
        require(amount > 0, "Amount must be greater than 0");
        // IERC20(tokenToaToken[token]).approve(address(pool), amount);
        pool.withdraw(token, amount, address(this));
        emit UnlockToken(token, address(this), amount);
    }

    receive() external payable {}
}
