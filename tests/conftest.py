#!/usr/bin/python3

import pytest
from brownie import web3, accounts
from scripts.help_scripts import get_account, fund_wallet


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def account():
    account = get_account()
    fund_wallet(account[1])
    return account


@pytest.fixture(scope="module")
def nonOwner():
    non_owner = accounts[2]
    fund_wallet(non_owner)
    return non_owner


@pytest.fixture(scope="module")
def contract(ZrxWallet, account):
    return ZrxWallet.deploy(1, {"from": account[1]})
