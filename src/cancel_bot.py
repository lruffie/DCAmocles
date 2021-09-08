from dotenv import load_dotenv
from binance.spot import Spot
import os
import json
import time
import asyncio

load_dotenv()

client = Spot(base_url='https://testnet.binance.vision',key=os.environ["API_KEY_TEST_NET"], secret=os.environ["API_KEY_TEST_NET_SECRET"])
       
# place first order :

cancel = client.cancel_open_orders(symbol="BTCUSDT")
print(cancel)
    
