from termcolor import cprint
import time
import json
import random
import requests
import ccxt.async_support as ccxt
from ccxt.base.errors import InvalidAddress, InvalidOrder, ExchangeError
import asyncio
import aiohttp

MIN_PRICE       = 1.5 # если цена ниже этой, продавать не будет

SYMBOL          = 'ARB' # сюда токен, который хотим слить
SELL_USDT       = 20 # сколько USDT продаем, чтобы купить SYMBOL, не трогаем, так как мы сливаем, а НЕ покупаем
TYPE_SIDE       = 'sell'
# PRICE           = 28000 # если хотим слить по конкретной цене. лучше не трогать
PRICE           = 'market' # если раскомментировать, тогда будет продавать по маркету
SPREAD          = 0.01 # на какой процент цена будет отличаться от маркета (выше / ниже в зависимости от TYPE_SIDE)
CHECK_PROFIT    = True # True / False. False если хочешь чуть чуть ускорить код, но тогда не будет писать в терминал на сколько продал монету
BREAK_DEF       = False # True / False. True если хочешь пройтись по аккаунтам 1 раз, False если хочешь смотреть баланс и продавать бесконечно. При TYPE_SIDE = buy, режим BREAK_DEF всегда = False

MIN_SELL        = 1 # если баланс монеты ниже этого числа, ордер на продажу выставлен не будет, не меняем
CALNCEL_ORDER   = True # True / False. если True, тогда через 3с после выставление лимитки ордер будет отменен (если он не был исполнен), не меняем

TIME_SLEEP      = 0.3 # сколько сек. спим между проверкой баланса

EXCHANGE = 'bybit' # вписываем нужную биржу (апи мекса говно и не дает возможности сливать), подходит ли биржа смотрим на https://github.com/ccxt/ccxt


ACCOUNTS = [
    {'name': '', 'apikey': '', 'apisecret': ''},
    ]

