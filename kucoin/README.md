# kucoin
grabs all the coins from kucoin, and automatically buys all coins that are under $1 USD value with btc balance

```sh
sudo pip install python-kucoin
```
- Go to [kucoin](https://www.kucoin.com/#/) and create [API Token](https://www.kucoin.com/#/user/setting/api)
- Fill in kucoin_key_secret_to_replace.json file with API Token created
- If there's btc balance on your account, simply run kucoin.py. Otherwise, transfer other types of currency onto the account and (ie, LTC) and use function `sellTargetCoin("LTC-BTC")` to convert it all to BTC
```sh
./kucoin.py
```
