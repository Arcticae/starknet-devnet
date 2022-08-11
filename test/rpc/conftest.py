"""
Fixtures for RPC tests
"""

from __future__ import annotations

import json
import typing

from test.util import load_file_content, run_devnet_in_background, terminate_and_wait

import pytest
from starkware.starknet.services.api.contract_class import ContractClass
from starkware.starknet.services.api.gateway.transaction import Transaction, Deploy

from .rpc_utils import gateway_call, add_transaction

DEPLOY_CONTENT = load_file_content("deploy_rpc.json")
INVOKE_CONTENT = load_file_content("invoke_rpc.json")
DECLARE_CONTENT = load_file_content("declare.json")


@pytest.fixture(name="contract_class")
def fixture_contract_class() -> ContractClass:
    """
    Make ContractDefinition from deployment transaction used in tests
    """
    transaction: Deploy = typing.cast(Deploy, Transaction.loads(DEPLOY_CONTENT))
    return transaction.contract_definition


@pytest.fixture(name="class_hash")
def fixture_class_hash(deploy_info) -> str:
    """
    Class hash of deployed contract
    """
    class_hash = gateway_call("get_class_hash_at", contractAddress=deploy_info["address"])
    return class_hash


@pytest.fixture(name="deploy_info")
def fixture_deploy_info() -> dict:
    """
    Deploy a contract on devnet and return deployment info dict
    """
    return add_transaction(json.loads(DEPLOY_CONTENT))


@pytest.fixture(name="invoke_info")
def fixture_invoke_info() -> dict:
    """
    Make an invoke transaction on devnet and return invoke info dict
    """
    invoke_tx = json.loads(INVOKE_CONTENT)
    invoke_tx["calldata"] = ["0"]
    invoke_info = add_transaction(invoke_tx)
    return {**invoke_info, **invoke_tx}


@pytest.fixture(name="declare_info")
def fixture_declare_info() -> dict:
    """
    Make a declare transaction on devnet and return declare info dict
    """
    declare_tx = json.loads(DECLARE_CONTENT)
    declare_info = add_transaction(declare_tx)
    return {**declare_info, **declare_tx}


@pytest.fixture(name="invoke_content", scope="module")
def fixture_invoke_content() -> dict:
    """
    Invoke content JSON object
    """
    return json.loads(INVOKE_CONTENT)


@pytest.fixture(name="deploy_content")
def fixture_deploy_content() -> dict:
    """
    Deploy content JSON object
    """
    return json.loads(DEPLOY_CONTENT)


@pytest.fixture(name="declare_content")
def fixture_declare_content() -> dict:
    """
    Declare content JSON object
    """
    return json.loads(DECLARE_CONTENT)


@pytest.fixture(name="run_devnet_in_background")
def fixture_run_devnet_in_background() -> dict:
    """
    Run devnet instance in background
    """
    proc = run_devnet_in_background()
    try:
        yield
    finally:
        terminate_and_wait(proc)
