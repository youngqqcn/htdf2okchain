#coding:utf8

# https://tronpy.readthedocs.io/en/latest/contract.html
from tronpy import Tron, Contract
from tronpy.keys import PrivateKey
import json

client = Tron(network='nile')
priv_key = PrivateKey(bytes.fromhex("7dc57026ffffb27e9f4eb97376f67a4156e40c41a55e57a3049b041db3d3d5f5"))



def main():

    bf = open('./bytecodes/bytecodes', 'r')
    bytecode = bf.read()
    # print(bytecode)
    bf.close()

    af = open('./abi/abi.json', 'r')
    abi = json.load(af)
    # print(abi)
    af.close()

    cntr = Contract(name="Orientwalt", bytecode=bytecode, abi=abi)

    txn = (
        client.trx.deploy_contract('TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk', cntr)
        .fee_limit(900_000_000)
        .build()
        .sign(priv_key)
    )
    print(txn)
    result = txn.broadcast().wait()
    print(result)
    print('Created:', result['contract_address'])
    created_cntr = client.get_contract(result['contract_address'])

    # created_cntr = client.get_contract('TAZV9R9rSd4pXUEP88qHt1r9thmQUEchhy')
    print(created_cntr.functions.balanceOf(who='TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk'))
    print(created_cntr.functions.owner())
    print(created_cntr.functions.totalSupply())

    pass

if __name__ == '__main__':
    main()

