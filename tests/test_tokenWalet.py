import brownie
from brownie import web3, accounts
from scripts.help_scripts import get_aToken_balance


def test_owner_deposit_token(contract, account, dai):
    value = web3.toWei("100", "ether")
    dai.approve(contract.address, value, {"from": account[1]})

    contract.depositToken(dai.address, value, {"from": account[1]})
    assert (
        contract.getTokenBalance(dai.address, {"from": account[1]})
        == value
    )
    assert dai.balanceOf(account[1]) == web3.toWei("400", "ether")


def test_owner_withdraw_token(contract, account, dai):
    value = web3.toWei("100", "ether")
    dai.approve(contract.address, value, {"from": account[1]})
    contract.depositToken(dai.address, value, {"from": account[1]})

    contract.withdrawToken(
        dai.address, web3.toWei("20", "ether"), {"from": account[1]}
    )
    assert contract.getTokenBalance(
        dai.address, {"from": account[1]}
    ) == web3.toWei("80", "ether")
    assert dai.balanceOf(account[1]) == web3.toWei("420", "ether")


def test_owner_transfer_token(contract, account, dai):
    value = web3.toWei("100", "ether")
    contract.depositEther({"from": account[1], "value": value})
    dai.approve(contract.address, value, {"from": account[1]})

    contract.depositToken(dai.address, value, {"from": account[1]})
    contract.transferToken(
        dai.address,
        account[3].address,
        web3.toWei("5", "ether"),
        {"from": account[1]},
    )
    assert contract.getTokenBalance(
        dai.address, {"from": account[1]}
    ) == web3.toWei("95", "ether")
    assert dai.balanceOf(account[3]) == web3.toWei("5", "ether")


def test_owner_lock_token(contract, account, dai):
    value = web3.toWei("100", "ether")
    lockValue = web3.toWei("50", "ether")
    dai.approve(contract.address, value, {"from": account[1]})
    contract.depositToken(dai.address, value, {"from": account[1]})
    contract.lockToken(dai.address, lockValue, {"from": account[1]})
    aDai = get_aToken_balance(
        "0x028171bCA77440897B824Ca71D1c56caC55b68A3", contract.address
    )

    assert dai.balanceOf(contract.address) == web3.toWei("50", "ether")
    assert aDai == web3.toWei("50", "ether")


def test_owner_unlock_token(contract, account, dai):
    value = web3.toWei("100", "ether")
    lockValue = web3.toWei("100", "ether")
    dai.approve(contract.address, value, {"from": account[1]})
    contract.depositToken(dai.address, value, {"from": account[1]})
    contract.lockToken(dai.address, lockValue, {"from": account[1]})

    contract.unlockToken(dai.address, lockValue, {"from": account[1]})
    aDai = get_aToken_balance(
        "0x028171bCA77440897B824Ca71D1c56caC55b68A3", contract.address
    )
    assert dai.balanceOf(contract.address) == value


def test_revert_deposit_token(contract, dai, nonOwner):
    value = web3.toWei("100", "ether")
    dai.approve(contract.address, value, {"from": nonOwner})
    with brownie.reverts():
        contract.depositToken(dai.address, value, {"from": nonOwner})
        contract.depositToken(
            dai.address, web3.toWei("0", "ether"), {"from": nonOwner}
        )
        contract.depositToken(
            web3.toChecksumAddress(
                "0x0000000000000000000000000000000000000000"
            ),
            value,
            {"from": nonOwner},
        )


def test_revert_withdraw_token(contract, dai, account, nonOwner):
    value = web3.toWei("100", "ether")
    dai.approve(contract.address, value, {"from": account[1]})
    with brownie.reverts():
        contract.withdrawToken(
            dai.address, web3.toWei("0", "ether"), {"from": account[1]}
        )

        contract.withdrawToken(
            web3.toChecksumAddress(
                "0x0000000000000000000000000000000000000000"
            ),
            value,
            {"from": account[1]},
        )

        contract.withdrawToken(
            dai.address,
            web3.toWei("500", "ether"),
            {"from": account[1]},
        )

        contract.withdrawToken(dai.address, value, {"from": nonOwner})


def test_revert_transfer_token(contract, dai, account, nonOwner):
    value = web3.toWei("100", "ether")
    dai.approve(contract.address, value, {"from": account[1]})
    with brownie.reverts():
        contract.transferToken(
            web3.toChecksumAddress(
                "0x0000000000000000000000000000000000000000"
            ),
            account[3],
            value,
            {"from": account[1]},
        )

        contract.transferToken(
            dai.address,
            web3.toChecksumAddress(
                "0x0000000000000000000000000000000000000000"
            ),
            value,
            {"from": account[1]},
        )

        contract.transferToken(
            dai.address,
            account[3],
            web3.toWei("0", "ether"),
            {"from": account[1]},
        )

        contract.transferToken(
            dai.address, account[3], value, {"from": nonOwner}
        )


def test_revert_lock_token(contract, dai, account, nonOwner):
    value = web3.toWei("100", "ether")
    lockValue = web3.toWei("50", "ether")
    dai.approve(contract.address, value, {"from": account[1]})

    with brownie.reverts():
        contract.lockToken(
            dai.address, web3.toWei("0", "ether"), {"from": account[1]}
        )
        contract.lockToken(
            dai.address,
            web3.toWei("150", "ether"),
            {"from": account[1]},
        )
        contract.lockToken(dai.address, lockValue, {"from": nonOwner})


def test_revert_unlock_token(contract, dai, account, nonOwner):
    value = web3.toWei("100", "ether")
    lockValue = web3.toWei("50", "ether")
    dai.approve(contract.address, value, {"from": account[1]})
    contract.depositToken(dai.address, value, {"from": account[1]})
    contract.lockToken(dai.address, lockValue, {"from": account[1]})

    with brownie.reverts():
        contract.unlockToken(
            dai.address, web3.toWei("0", "ether"), {"from": account[1]}
        )
        contract.unlockToken(
            dai.address,
            web3.toWei("150", "ether"),
            {"from": account[1]},
        )
        contract.unlockToken(dai.address, lockValue, {"from": nonOwner})
