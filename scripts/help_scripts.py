from brownie import network, accounts, config, web3, interface, Contract
import json


def get_account():
    if network.show_active() in config["networks"]:
        account = accounts.from_mnemonic(
            mnemonic=config["wallets"]["from_mnemonic"], count=5
        )
        return account
    return None


def fund_wallet(wallet):
    funds_wallet = accounts[10]
    tx = funds_wallet.transfer(wallet, web3.toWei("500", "ether"))
    print("Funded {}".format(wallet))
    return tx


def fund_token(wallet):
    token_address = config["networks"][network.show_active()]["dai"]
    token = Contract.from_explorer(token_address)
    tx = token.transfer(
        wallet, web3.toWei("500", "ether"), {"from": accounts[10]}
    )


def get_aToken_balance(tokenAddress, wallet):
    token = interface.IERC20(tokenAddress)
    return token.balanceOf(wallet)


def get_token_data():
    token = []
    atoken = []
    with open("scripts/aave-mainnet.json", "r") as data:
        aave_address = json.load(data)
    for i in range(len(aave_address)):
        token.append(aave_address[i]["address"])
        atoken.append(aave_address[i]["aTokenAddress"])
    return token, atoken
