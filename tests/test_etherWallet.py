import brownie
from brownie import web3, accounts


def test_owner_deposit_ether(contract, account):
    value = web3.toWei("100", "ether")
    contract.depositEther({"from": account[1], "value": value})
    assert contract.balance() == value


def test_owner_withdraw_ether(contract, account):
    deposit_value = web3.toWei("50", "ether")
    contract.depositEther({"from": account[1], "value": deposit_value})

    contract.withdrawEther(
        web3.toWei("5", "ether"), {"from": account[1]}
    )
    assert contract.balance() == web3.toWei("45", "ether")


def test_owner_transfer_ether(contract, account, nonOwner):
    deposit_value = web3.toWei("50", "ether")
    contract.depositEther({"from": account[1], "value": deposit_value})

    contract.transferEther(
        accounts[3], web3.toWei("5", "ether"), {"from": account[1]}
    )
    assert contract.balance() == web3.toWei("45", "ether")
    assert accounts[3].balance() == web3.toWei("105", "ether")


def test_revert_deposit_ether(contract, account, nonOwner):
    with brownie.reverts():
        contract.depositEther(
            {"from": nonOwner, "value": web3.toWei("1", "ether")}
        )
        contract.depositEther(
            {"from": account[1], "value": web3.toWei("0", "ether")}
        )


def test_revert_withdraw_ether(contract, account, nonOwner):
    deposit_value = web3.toWei("50", "ether")
    contract.depositEther({"from": account[1], "value": deposit_value})

    with brownie.reverts():
        contract.withdrawEther(deposit_value, {"from": nonOwner})
        contract.withdrawEther(
            web3.toWei("0", "ether"), {"from": account[1]}
        )
        contract.withdrawEther(
            web3.toWei("70", "ether"), {"from": account[1]}
        )


def test_revert_transfer_ether(contract, account, nonOwner):
    deposit_value = web3.toWei("50", "ether")
    contract.depositEther({"from": account[1], "value": deposit_value})

    with brownie.reverts():
        contract.transferEther(
            accounts[3], web3.toWei("5", "ether"), {"from": nonOwner}
        )
        contract.transferEther(
            accounts[3], web3.toWei("0", "ether"), {"from": account[1]}
        )
        contract.transferEther(
            accounts[3], web3.toWei("70", "ether"), {"from": account[1]}
        )
