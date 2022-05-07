from brownie import network, accounts, config, web3, Contract


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
