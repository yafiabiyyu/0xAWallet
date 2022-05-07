#!/usr/bin/python3

import pytest
from brownie import web3, accounts, config, network, Contract
from scripts.help_scripts import get_account, fund_wallet, fund_token


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def dai():
    dai_address = config["networks"][network.show_active()]["dai"]
    dai = Contract.from_explorer(dai_address)
    return dai


@pytest.fixture(scope="module")
def account():
    account = get_account()
    fund_wallet(account[1])
    fund_token(account[1])
    return account


@pytest.fixture(scope="module")
def nonOwner():
    non_owner = accounts[2]
    fund_wallet(non_owner)
    fund_token(non_owner)
    return non_owner


@pytest.fixture(scope="module")
def contract(ZrxWallet, account):
    return ZrxWallet.deploy({"from": account[1]})
