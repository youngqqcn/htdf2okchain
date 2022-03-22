#coding:utf8

from tronpy import Tron, Contract
from tronpy.keys import PrivateKey
import json


def freeze_balance():

    client = Tron(network='nile')
    priv_key = PrivateKey(bytes.fromhex("7dc57026ffffb27e9f4eb97376f67a4156e40c41a55e57a3049b041db3d3d5f5"))
    tx = client.trx.freeze_balance(
        owner='TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk',
        amount=500_000_000,
        resource="ENERGY",
        # receiver='TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk',
        ).fee_limit(50_000_000).build().sign(priv_key)

    res = tx.broadcast().wait()
    print(res)

    pass


def main():
    freeze_balance()
    pass


if __name__ == '__main__':
    main()
