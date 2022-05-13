from brownie import network, ZrxWallet, web3, config, network, interface
from scripts.help_scripts import (
    get_account,
    get_aToken_balance,
    get_token_data,
)


def main():
    account = get_account()
    token, atoken = get_token_data()
    value = web3.toWei("500", "ether")
    IlendingPoolProvider = config["networks"][network.show_active()][
        "LendingPoolAddressProvider"
    ]
    LendingPool = config["networks"][network.show_active()][
        "LendingPoolAddress"
    ]
    WethGateway = config["networks"][network.show_active()][
        "WethGateway"
    ]
    aWeth = config["networks"][network.show_active()]["aweth"]
    contract = ZrxWallet.deploy(
        token,
        atoken,
        IlendingPoolProvider,
        LendingPool,
        WethGateway,
        aWeth,
        {"from": account[0]},
        publish_source=True,
    )
    contract.tx.wait(10)
    depoTx = contract.depositEther(
        {"from": account[0], "value": web3.toWei("0.1", "ether")}
    )
    depoTx.wait(10)

    token = interface.IERC20(
        config["networks"][network.show_active()]["dai"]
    )
    token.approve(contract.address, value, {"from": account[0]})

    depoTokenTx = contract.depositToken(
        token.address, value, {"from": account[0]}
    )
    depoTokenTx.wait(10)
