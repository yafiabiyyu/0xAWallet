import brownie
from brownie import web3


def test_owner_deposit_ether(contract, account):
    deposit = web3.toWei(1, "ether")
    contract.depositEther({"from": account[1], "value": deposit})
    assert contract.getEtherBalance({"from": account[1]}) == deposit


def test_owner_withdraw_ether(contract, account):
    balance = web3.toWei("2", "ether")
    contract.depositEther({"from": account[1], "value": balance})

    contract.withdrawEther(
        web3.toWei("2", "ether"), {"from": account[1]}
    )

    assert contract.getEtherBalance({"from": account[1]}) == 0


def test_owner_withdraw_ether_greter_balance(contract, account):
    balance = web3.toWei("2", "ether")
    contract.depositEther({"from": account[1], "value": balance})
    with brownie.reverts():
        contract.withdrawEther(
            web3.toWei("11", "ether"), {"from": account[1]}
        )


def test_non_owner_update_claim_periode(contract, account):
    with brownie.reverts():
        contract.updateClaimPeriod(2, {"from": account[2]})


def test_non_owner_deposit_ether(contract, nonOwner):
    balance = web3.toWei("2", "ether")
    with brownie.reverts():
        contract.depositEther({"from": nonOwner, "value": balance})


def test_non_owner_withdraw_ether(contract, nonOwner):
    with brownie.reverts():
        contract.withdrawEther(
            web3.toWei("2", "ether"), {"from": nonOwner}
        )
