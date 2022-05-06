from brownie import network, accounts, config, web3


def get_account():
    if network.show_active() in config["networks"]:
        account = accounts.from_mnemonic(
            mnemonic=config["wallets"]["from_mnemonic"], count=5
        )
        return account
    return None


def fund_wallet(wallet):
    funds_wallet = accounts[11]
    tx = funds_wallet.transfer(wallet, web3.toWei("3", "ether"))
    print("Funded {}".format(wallet))
    return tx
