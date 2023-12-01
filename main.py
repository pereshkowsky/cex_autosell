from config import *


async def sell(account, name):

    while True:
            
        try:

            if CHECK_PROFIT == True:
                try:
                    check_balance      = await account.fetch_balance()
                    usdt_balance_start = check_balance['USDT']['free']
                except Exception as error: 
                    cprint(error, 'red')

            pair = f'{SYMBOL}/USDT'

            # check balance
            if TYPE_SIDE == 'sell':
                while True:
                    try:
                        check_balance   = await account.fetch_balance()
                        balance_of_coin = check_balance[SYMBOL]['free']
                        cprint(f"{name} | balance of {SYMBOL} : {balance_of_coin}", 'blue')
                        if balance_of_coin > 0 : break
                        await asyncio.sleep(TIME_SLEEP)
                    except: 
                        cprint(f"{name} | balance of {SYMBOL} : 0", 'blue')
                        await asyncio.sleep(TIME_SLEEP)


            if PRICE == 'market':
                while True:
                    try:
                        # check book of pair 
                        order_book = await account.fetch_order_book(pair)
                        order_bids = order_book['bids'][0][0]
                        order_asks = order_book['asks'][0][0]

                        if TYPE_SIDE   == 'buy' : price_to_order = order_asks + order_asks * SPREAD
                        elif TYPE_SIDE == 'sell': price_to_order = order_bids - order_bids * SPREAD
                        break
                    except Exception as error:
                        cprint(f'{name} | ckeck_price error : {error}', 'red')
                        time.sleep(0.5)

            else : price_to_order = PRICE


            try:

                # make an order
                if TYPE_SIDE == 'buy':

                    order = await account.create_limit_buy_order(
                        symbol = pair,
                        amount = SELL_USDT / price_to_order,
                        price  = price_to_order,
                        params = {}
                    )

                elif TYPE_SIDE == 'sell':

                    if balance_of_coin > MIN_SELL:

                        if price_to_order >= MIN_PRICE:

                            order = await account.create_limit_sell_order(
                                symbol = pair,
                                amount = balance_of_coin,
                                price  = price_to_order,
                                params = {}
                            )

                        else : cprint(f'>>> current price {price_to_order} < MIN_PRICE {MIN_PRICE}', 'yellow')

            except Exception as error:
                cprint(f'{name} | create_order error : {error}', 'red')

            
            if CHECK_PROFIT == True:
                try:

                    check_balance = await account.fetch_balance()
                    usdt_balance = check_balance['USDT']['free']

                    if TYPE_SIDE == 'buy':
                        result = usdt_balance_start - usdt_balance
                        cprint(f'>>> {name} | {TYPE_SIDE} {SYMBOL} | {int(result)} USDT', 'yellow')
                    elif TYPE_SIDE == 'sell':
                        result = usdt_balance - usdt_balance_start
                        if balance_of_coin > MIN_SELL:
                            if price_to_order >= MIN_PRICE:
                                cprint(f'>>> {name} | {TYPE_SIDE} {SYMBOL} | {int(result)} USDT', 'yellow')
                

                except Exception as error:
                    cprint(f'{name} | error : {error}', 'red')


            if CALNCEL_ORDER == True:
                if TYPE_SIDE == 'sell':
                    if balance_of_coin > MIN_SELL:
                        if price_to_order >= MIN_PRICE:
                            try:
                                await asyncio.sleep(3)
                                await account.cancel_order(order['id'], order['symbol'])
                            except : cprint(f'{name} | cancel_order error', 'red')


            if TYPE_SIDE == 'sell':
                if BREAK_DEF == True:
                    break
            else : break

        
        except Exception as error:
            cprint(f'{name} | {error}', 'red')

    await account.close()


async def main():

    start = float(time.perf_counter())

    tasks = []

    for data in ACCOUNTS:

        name        = data['name']
        api_key     = data['apikey']
        api_secret  = data['apisecret']

        headers = {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        }

        account = ccxt.__dict__[EXCHANGE](headers)

        task = asyncio.create_task(sell(account, name))
        tasks.append(task)

    await asyncio.gather(*tasks)


    fin = round((time.perf_counter() - start), 1)
    cprint(f'result : {fin} sec', 'white')


asyncio.run(main())

