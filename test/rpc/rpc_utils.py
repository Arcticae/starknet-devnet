"""
Utilities for RPC tests
"""

from __future__ import annotations

from typing import Union
import requests

from ..settings import APP_URL


class BackgroundDevnetClient:
    """ A thin wrapper for requests, to interact with a background devnet instance """

    @staticmethod
    def get(endpoint: str) -> requests.Response:
        """ Submit get request at given endpoint """
        return requests.get(f"{APP_URL}{endpoint}", headers={"content-type": "application/json"})

    @staticmethod
    def post(endpoint: str, body: dict) -> requests.Response:
        """ Submit post request with given dict in body (JSON) """
        return requests.post(f"{APP_URL}{endpoint}", json=body)


def rpc_call(method: str, params: Union[dict, list]) -> dict:
    """
    Make a call to the RPC endpoint
    """
    req = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 0
    }

    response = BackgroundDevnetClient.post(
        "/rpc",
        body=req
    )
    return response.json()


def add_transaction(body: dict) -> dict:
    """
    Make a call to the RPC endpoint
    """
    response = BackgroundDevnetClient.post('/gateway/add_transaction', body)
    return response.json()


def gateway_call(method: str, **kwargs):
    """
    Make a call to the gateway
    """
    response = BackgroundDevnetClient.get(
        f"/feeder_gateway/{method}?{'&'.join(f'{key}={value}&' for key, value in kwargs.items())}"
    )
    return response.json()


def get_block_with_transaction(transaction_hash: str) -> dict:
    """
    Retrieve block for given transaction
    """
    transaction = gateway_call("get_transaction", transactionHash=transaction_hash)
    assert transaction["status"] != "NOT_RECEIVED", f"Transaction {transaction_hash} was not received or does not exist"
    block_number: int = transaction["block_number"]
    block = gateway_call("get_block", blockNumber=block_number)
    return block


def pad_zero(felt: str) -> str:
    """
    Convert felt with format `0xValue` to format `0x0Value`
    """
    felt = felt.lstrip("0x")
    return "0x0" + felt
