
https://www.oklink.com/zh-cn/oec/token-list

https://docs.klend.finance/klend/help/oec

https://github.com/okex/exchain


https://okexchain-docs.readthedocs.io/

https://okexchain-docs.readthedocs.io/en/latest/developers/basics/accounts.html

# ~~HTDF资产迁移到OkChain的KIP20~~

# HTDF资产迁移到波场链
## 1、可行性研究


### 地址映射



ETH私钥生成公钥
```python

privKey = '7dc57026ffffb27e9f4eb97376f67a4156e40c41a55e57a3049b041db3d3d5f5'

sk = ecdsa.SigningKey.from_string(unhexlify(privKey), curve=ecdsa.SECP256k1) #通过私钥生成密钥对
pubKey = hexlify(sk.verifying_key.to_string())   #获取公钥

print(sk.verifying_key.to_string(encoding='compressed').hex())

```


输出公钥：`03c0db929607303c8106ab8bc2add8648eb6b78d37d6d0e0caa31455a64e3ff6b0`



借鉴Okchain公钥到地址的转换

```go
func (key PubKey) Address() tmcrypto.Address {
	pubk, err := ethcrypto.DecompressPubkey(key)
	if err != nil {
		panic(err)
	}

	return tmcrypto.Address(ethcrypto.PubkeyToAddress(*pubk).Bytes())
}



func PubkeyToAddress(p ecdsa.PublicKey) common.Address {
	pubBytes := FromECDSAPub(&p)
	return common.BytesToAddress(Keccak256(pubBytes[1:])[12:])
}

```


HTDF从公钥推导出ETH地址


```go

// query accountREST Handler
func QueryAccountRequestHandlerFn(
	storeName string, cdc *codec.Codec,
	decoder auth.AccountDecoder, cliCtx context.CLIContext,
) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		bech32addr := vars["address"]

		addr, err := sdk.AccAddressFromBech32(bech32addr)
		if err != nil {
			rest.WriteErrorResponse(w, http.StatusInternalServerError, err.Error())
			return
		}

		res, err := cliCtx.QueryStore(auth.AddressStoreKey(addr), storeName)
		if err != nil {
			rest.WriteErrorResponse(w, http.StatusInternalServerError, err.Error())
			return
		}

		// the query will return empty if there is no data for this account
		if len(res) == 0 {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		// decode the value
		account, err := decoder(res)
		if err != nil {
			rest.WriteErrorResponse(w, http.StatusInternalServerError, err.Error())
			return
		}

		// json message
		var acc AccountBodyEx
		acc.Type = "auth/Account"

		var AccInfo NewAccInfoEx

		if true {

			//unit shift
			AccInfo.Address = account.GetAddress()
			AccInfo.Coins = unit_convert.DefaultCoinsToBigCoins(account.GetCoins())
			AccInfo.PubKey = account.GetPubKey()
			//===============Debug=======================
			// fmt.Printf("===address===>%v", hex.EncodeToString(account.GetPubKey().Address()))
			if pub, ok := AccInfo.PubKey.(secp256k1.PubKeySecp256k1); ok {
				pubk, err := ethcrypto.DecompressPubkey(pub[:])
				if err != nil {
					panic(err)
				}
				fmt.Printf("pub1: %v\n", pub.String())
				pb := ethcrypto.FromECDSAPub(pubk)
				fmt.Printf("pub_uncompressed: %v\n", hex.EncodeToString(pb[2:])) // ignore 04 prefix
				AccInfo.RawPubKey = hex.EncodeToString(pb[2:])
				AccInfo.HexAddress = ethcrypto.PubkeyToAddress(*pubk).String()
			}
			// AccInfo.HexAddress = ethcmn.BytesToAddress(account.GetPubKey().Address().Bytes()).String()
			//===============Debug=======================
			AccInfo.AccountNumber = account.GetAccountNumber()
			AccInfo.Sequence = account.GetSequence()
		}
		acc.Value = AccInfo

		rest.PostProcessResponse(w, cdc, acc, cliCtx.Indent)

	}
}

```

ETH地址
私钥：7dc57026ffffb27e9f4eb97376f67a4156e40c41a55e57a3049b041db3d3d5f5
公钥：03c0db929607303c8106ab8bc2add8648eb6b78d37d6d0e0caa31455a64e3ff6b0
公钥（未压缩）：04c0db929607303c8106ab8bc2add8648eb6b78d37d6d0e0caa31455a64e3ff6b0e082af9242fb88b7544759dcadd7d9f299f3b1376e1459cdd6029c5d12d7dc0b
eth地址：0x4ae081212C56492FA320338a3A64E346AB75F39B

通过RPC接口可以查询到地址的pubkey，

> 注意：仅有在HTDF2.0上转过账户才能查询到pubkey


转TRON的地址

```python
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

```




运行结果

```
TGo7x6S8FA8uRZYvyT9U1ZV4yXDYUUxAyk
4ae081212c56492fa320338a3a64e346ab75f39b
```

## 2、如何迁移？


目前，迁移方案主要有2种：

#### 方案1：主动迁移

由用户主动发起，在HTDF公链向黑洞地址进行转账进行HTDF销毁，由机器人监测，并由机器人在TRON向用户地址在TRON映射的地址，进行自动等量空投。

例如：用户在HTDF公链销毁500HTDF，机器人监测到这笔交易，自动在TRON对其对应的地址进行空投 500 KIP20-HTDF。


另外，用户交易所的HTDF资产，则不需要进行任何操作，交易所会帮用户进行迁移。


#### ~~方案2：被动迁移（尚不完善）~~


~~此方案只能适用于那些在HTDF2.0上进行过转账的地址，因为那些没有在HTDF2.0转过帐的地址无法获取其公钥，所以，无法推导出其在OK链上的映射地址，无法空投。~~



### 2.2、TRC20-HTDF资产的发行总量及流通量的问题

- 保持`96,000,000`总的发行量恒定不变
- 取消挖矿机制，流通量等于总发行量


### 2.3、迁移资产的问题

迁移资产分以下2类：
- 普通账户的资产：`迁移资产 = 账户余额 + 委托金额 + 委托收益`
- 超级管理员资产：`总发行量 - 普通账户总资产`


### 2.4、如何获取链上所有普通账户的资产？

节点使用命令 `hsd export > genesis.json` 导出链上的状态。`genesis.json`包含了账户的`账户余额` 、`委托金额`,但是没有`委托收益`。


解决方案： `委托收益`可以通过RPC接口查询获得

### 2.5、正在解除委托中的资产如何获取？



