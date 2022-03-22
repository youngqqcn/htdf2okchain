from tronpy import Tron, Contract
from tronpy.keys import PrivateKey

# client = Tron(network='mainnet')
client = Tron(network='nile')


# # 3b27180746e68744e5e2e981ae6fa54d502f2aa6e18b8a98824fd1a69069d55a


tx = client.get_transaction(txn_id='a30b13f0e16d31705ab7eb633260850178708d9494e79dd79c1b2b29b1baf811')
print(tx)
