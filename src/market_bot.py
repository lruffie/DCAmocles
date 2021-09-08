from dotenv import load_dotenv
from binance.spot import Spot
import os
import json
import time
import asyncio

load_dotenv()


# client = Spot(base_url='https://testnet.binance.vision',key=os.environ["API_KEY_TEST_NET_PUBLIC"], secret=os.environ["API_KEY_TEST_NET_SECRET"])
client = Spot(base_url='https://api.binance.com',key=os.environ["API_KEY_MAIN_NET_PUBLIC"], secret=os.environ["API_KEY_MAIN_NET_SECRET"])

# place first order :


# price=3000
# symb="ETHUSDT"
# amount=0.01
# order=client.new_order(symbol=symb, side="BUY", type="MARKET", quantity=amount)
# print(order)

# order= client.get_open_orders()
# print(order)


info = client.exchange_info()

# print(info)

symb='SOLBUSD'

for pair in info['symbols']:
    if pair['symbol'] == symb :
        print(pair)
        info1 = pair
        precision = pair['baseAssetPrecision']




# price=48000
# stopPrice=price
# symb="BTCUSDT"
# amount=0.001
# print(client.ticker_price(symb))
# order = client.new_order(symbol=symb ,side="SELL", type="STOP_LOSS_LIMIT", quantity=amount ,price=price, stopPrice=price-1, timeInForce='GTC')
# print(order)
    

# bot=Bot(level=3100,asset="BTC", amount=0.01, base="BUSD", side="SELL", delta=0.1, api_key=os.environ["API_KEY_TEST_NET"],api_secret=os.environ["API_KEY_TEST_NET_SECRET"])

# print(bot.check_balance())

# print(bot.place_order())
# time.sleep(2)
# print(bot.track_order())
# time.sleep(2)
# print(bot.track_all_orders())
# time.sleep(2)
# print(bot.cancel_all_orders())
# time.sleep(2)
# print(bot.cancel_order())



# print(bot.comparison())

# print(bot.track_all_orders())
# hb=binance_listen.Heartbeat(asset="ETH", base="USDT",  api_key=os.environ["API_KEY_BINANCE"],api_secret=os.environ["API_KEY_BINANCE_SECRET"])


# asyncio.run(hb.main())

# time.sleep(2)
# print(bot.cancel_all_orders())
# print("done")