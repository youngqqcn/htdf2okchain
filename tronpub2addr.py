# coding:utf8
from binascii import unhexlify
from tronpy.keys import PublicKey


def main():
    # privkey = PrivateKey(unhexlify('7dc57026ffffb27e9f4eb97376f67a4156e40c41a55e57a3049b041db3d3d5f5'))
    pubkey = PublicKey(unhexlify('c0db929607303c8106ab8bc2add8648eb6b78d37d6d0e0caa31455a64e3ff6b0e082af9242fb88b7544759dcadd7d9f299f3b1376e1459cdd6029c5d12d7dc0b'))
    print(pubkey.to_base58check_address())
    print(pubkey.to_tvm_address().hex()) # tvm地址 
    # print(pubkey.to_hex_address())

    pass

if __name__ == '__main__':
    main()

