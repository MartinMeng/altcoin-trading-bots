#!/usr/bin/env python

"""
    * How to deal with fees?
"""

import os, json, time, math
from kucoin.client import Client

USD = 'USD'
NEGLIGIBLE_AMOUNT = 0.0001

"""
    @param pair: ie, LTC-BTC
    @param balance: amount of (usually btc) to spend buying the target coin
    buys LTC with specified BTC balance
"""
def buyTargetCoin(pair, balance):
    sellCoin = pair.split("-")[1]; buyCoin = pair.split("-")[0]
    while balance > NEGLIGIBLE_AMOUNT:
        sellOrders = client.get_sell_orders(pair, limit=1)
        sellOrder = sellOrders[0]
        sellBalance = min(balance * 0.999, sellOrder[1])  # either spend all remaining balance or fill the entire order
        buyAmount = sellBalance / sellOrder[0]
        transaction = client.create_buy_order(pair, str(sellOrder[0]), str(math.floor(buyAmount)))
        if transaction != None:
            print transaction
            print "Bought: {0}[{1}]; Sold {2}[{3}]; at a rate of: {4}[{5}]".format(buyCoin, buyAmount, sellCoin, sellBalance, pair, sellOrder[0])
            balance -= sellBalance * 1.001
        else:
            print "Transaction didn't go through for: {0}".format(pair)
        time.sleep(3)

"""
    @param pair: ie, LTC-BTC
    sells all LTC balance for BTC
"""
def sellTargetCoin(pair):
    sellCoin = pair.split("-")[0]; buyCoin = pair.split("-")[1]
    balance = client.get_coin_balance(sellCoin)["balance"]
    while balance > NEGLIGIBLE_AMOUNT:
        buyOrders = client.get_buy_orders(pair, limit=1)
        buyOrder = buyOrders[0]
        sellAmount = min(balance * 0.999, buyOrder[1])
        buyAmount = sellAmount * buyOrder[0]
        transaction = client.create_sell_order(pair, buyOrder[0], sellAmount)
        if transaction != None:
            print transaction
            print "Sold {0}[{1}]; Bought: {2}[{3}]; at a rate of: {4}[{5}]".format(sellCoin, sellAmount, buyCoin, buyAmount, pair, buyOrder[0])
        else:
            print "Transaction didn't go through"
        time.sleep(3)
        balance = client.get_coin_balance(sellCoin)["balance"]

keySecret = json.load(open('kucoin_key_secret.json'))
client = Client(keySecret['key'], keySecret['secret'])
symbolTicks = client.get_trading_symbols()
coinToTicker = {}

for symbolTick in symbolTicks:
    coinName = str(symbolTick["coinType"])
    if coinName not in coinToTicker.keys():
        coinToTicker[coinName] = []
    coinToTicker[coinName].append(str(symbolTick["symbol"]))

currencyPrices = client.get_currencies(coinToTicker.keys())['rates']
"""
allCoins = [str(coin) for coin in currencyPrices.keys()]
allCoins.sort()
print allCoins, len(allCoins)
"""
targetCoins = [str(coin) for coin in currencyPrices.keys() if currencyPrices[coin][USD] < 1]
targetCoins.sort()
print targetCoins
numTargetCoins = len(targetCoins)
print numTargetCoins

btcBalance = client.get_coin_balance("BTC")['balance']
btcBalanceSlice = float(btcBalance) / numTargetCoins
print "total btc balance {0}, per slice btc balance: {1}".format(btcBalance, btcBalanceSlice)

for targetCoin in targetCoins:
    pair = "{0}-BTC".format(str(targetCoin))
    buyTargetCoin(pair, btcBalanceSlice)
