#coding:utf8

from bech32 import bech32_decode, convertbits

def bech32_to_hexaddr(bech32_address: str) -> str:
    assert len(bech32_address) > 0
    _, data = bech32_decode(bech32_address)
    hexbytes = convertbits(data, 5, 8, pad=False)
    hexstraddr = ''.join(['%02x' % x for x in hexbytes])
    return hexstraddr.upper()


#例如：https://www.oklink.com/zh-cn/oec/address/0xaa569a9dca7ef274de69e6527440bfd55744f9b3
def main():
    print(bech32_to_hexaddr('ex14ftf48w20me8fhnfuef8gs9l64t5f7dnsdt9th'))

if __name__ == '__main__':
    main()
