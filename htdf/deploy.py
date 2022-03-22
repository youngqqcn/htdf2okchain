#coding:utf8

# https://tronpy.readthedocs.io/en/latest/contract.html
from tronpy import Tron, Contract
from tronpy.keys import PrivateKey
import json

client = Tron(network='nile')
priv_key = PrivateKey(bytes.fromhex("7dc57026ffffb27e9f4eb97376f67a4156e40c41a55e57a3049b041db3d3d5f5"))
# priv_key = PrivateKey(bytes.fromhex("04f73c190f8143c8abe8b3d85e8c4faf1d148c43f261a89793398c370851e48d"))



def main():

    # bf = open('./bytecodes/bytecodes', 'r')
    # bytecode = bf.read()
    # # print(bytecode)
    # bf.close()

    # af = open('./abi/abi.json', 'r')
    # abi = json.load(af)
    # # print(abi)
    # af.close()

    # # 关于用户承担资源比例，可以看
    # #  https://tronprotocol.github.io/documentation-zh/mechanism-algorithm/resource/
    # cntr = Contract(name="Orientwalt", bytecode=bytecode, abi=abi,
    #     user_resource_percent=0)

    # txn = (
    #     client.trx.deploy_contract('TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk', cntr)
    #     .fee_limit(900_000_000)
    #     .build()
    #     .sign(priv_key)
    # )
    # print(txn)
    # result = txn.broadcast().wait()
    # print(result)
    # print('Created:', result['contract_address'])
    # created_cntr = client.get_contract(result['contract_address'])

    created_cntr = client.get_contract('TLtojNebfACbSk929zueNd1YR4FcwNjFNj')
    print(created_cntr.functions.balanceOf(who='TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk'))
    print(created_cntr.functions.owner())
    print(created_cntr.functions.totalSupply())

    tx = created_cntr.functions.transfer(_to='TX2cQJ8qK6EGxsyZbP2aVAJ5YzpCZFPvWg', _value=1000000000).with_owner('TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk')\
    .fee_limit(50_000_000)\
    .build()\
    .sign(priv_key)
    res = tx.broadcast().wait()
    print(res)

    pass

if __name__ == '__main__':
    main()

