
https://www.oklink.com/zh-cn/oec/token-list

https://docs.klend.finance/klend/help/oec

https://github.com/okex/exchain


https://okexchain-docs.readthedocs.io/

# HTDF资产迁移到OkChain的KIP20

## 1、可行性研究


### 私钥和地址的映射

因为OkChain和HTDF一样也是基于CosmosSDK开发，所以私钥生成地址的方式相同

代码验证


例如：https://www.oklink.com/zh-cn/oec/address/0xaa569a9dca7ef274de69e6527440bfd55744f9b3

```python
#coding:utf8

from bech32 import bech32_decode, convertbits

def bech32_to_hexaddr(bech32_address: str) -> str:
    assert len(bech32_address) > 0
    _, data = bech32_decode(bech32_address)
    hexbytes = convertbits(data, 5, 8, pad=False)
    hexstraddr = ''.join(['%02x' % x for x in hexbytes])
    return hexstraddr.upper()

def main():
    print(bech32_to_hexaddr('ex14ftf48w20me8fhnfuef8gs9l64t5f7dnsdt9th'))

if __name__ == '__main__':
    main()

```

运行结果

```
AA569A9DCA7EF274DE69E6527440BFD55744F9B3
```

Okchain的bech32地址 `ex14ftf48w20me8fhnfuef8gs9l64t5f7dnsdt9th` 转为普通地址 `0xaa569a9DcA7eF274de69E6527440Bfd55744F9B3`，和python示例运行结果完全一样。

那么，从HTDF的`htdf`前缀开头的bech32格式的地址转换到okchain的普通地址方式也是一样的。

例如，以地址`htdf1jrh6kxrcr0fd8gfgdwna8yyr9tkt99ggmz9ja2`为例，转为OkChain普通地址为`0x90EFAB18781BD2D3A1286BA7D390832AECB29508`。


综上所述，从技术上证明了可以保持HTDF账户的私钥不变，将HTDF链上的账户资产映射到OkChain的KIP20上。


## 2、如何迁移？

### 2.1、KIP20-HTDF资产的发行总量及流通量的问题

- 保持`96,000,000`总的发行量恒定不变
- 取消挖矿机制，流通量等于总发行量


### 2.2、迁移资产的问题

迁移资产分以下2类：
- 普通账户的资产：`迁移资产 = 账户余额 + 委托金额 + 委托收益`
- 超级管理员资产：`总发行量 - 普通账户总资产`


### 2.3、如何获取链上所有普通账户的资产？

节点使用命令 `hsd export > genesis.json` 导出链上的状态。`genesis.json`包含了账户的`账户余额` 、`委托金额`,但是没有`委托收益`。


解决方案： `委托收益`可以通过RPC接口查询获得

### 2.4、正在解除委托中的资产如何获取？


