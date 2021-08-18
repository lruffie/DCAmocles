from dotenv import load_dotenv
from binance.spot import Spot
import os
import json
import time
import asyncio
import binance_listen

load_dotenv()


client = Spot(base_url='https://testnet.binance.vision',key=os.environ["API_KEY_TEST_NET"], secret=os.environ["API_KEY_TEST_NET_SECRET"])
       
# place first order :


price=3000
symb="BTCUSDT"
amount=0.001
order=client.new_order(symbol=symb, side="BUY", type="MARKET", quantity=amount)
print(order)




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