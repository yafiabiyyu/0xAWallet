import brownie
from brownie import web3, accounts
from scripts.help_scripts import get_aToken_balance


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


def test_owner_lock_ether(contract, account):
    value = web3.toWei("100", "ether")
    contract.depositEther({"from": account[1], "value": value})

    contract.lockEther(web3.toWei("50", "ether"), {"from": account[1]})
    balance = get_aToken_balance(
        "0x030bA81f1c18d280636F32af80b9AAd02Cf0854e", contract.address
    )
    assert contract.balance() == web3.toWei("50", "ether")
    assert balance == web3.toWei("50", "ether")


def test_owner_unlock_ether(contract, account):
    value = web3.toWei("100", "ether")
    contract.depositEther({"from": account[1], "value": value})
    contract.lockEther(web3.toWei("50", "ether"), {"from": account[1]})

    contract.unlockEther(
        web3.toWei("25", "ether"), {"from": account[1]}
    )
    balance = get_aToken_balance(
        "0x030bA81f1c18d280636F32af80b9AAd02Cf0854e", contract.address
    )
    assert contract.balance() == web3.toWei("75", "ether")
    # assert balance >= web3.toWei("25", "ether")


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


def test_revert_lock_ether(contract, account, nonOwner):
    value = web3.toWei("100", "ether")
    contract.depositEther({"from": account[1], "value": value})

    with brownie.reverts():
        contract.lockEther(
            web3.toWei("0", "ether"), {"from": account[1]}
        )
        contract.lockEther(
            web3.toWei("150", "ether"), {"from": account[1]}
        )
        contract.lockEther(
            web3.toWei("50", "ether"), {"from": nonOwner}
        )


def test_revert_unlock_ether(contract, account, nonOwner):
    value = web3.toWei("100", "ether")
    contract.depositEther({"from": account[1], "value": value})
    contract.lockEther(web3.toWei("50", "ether"), {"from": account[1]})

    with brownie.reverts():
        contract.unlockEther(
            web3.toWei("0", "ether"), {"from": account[1]}
        )
        contract.unlockEther(
            web3.toWei("150", "ether"), {"from": account[1]}
        )
        contract.unlockEther(
            web3.toWei("50", "ether"), {"from": nonOwner}
        )
