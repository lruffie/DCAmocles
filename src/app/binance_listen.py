from dotenv import load_dotenv
from binance.spot import Spot
import time
import os
import json
import asyncio

load_dotenv()

class Heartbeat:
    def __init__(self, asset, base, api_key, api_secret):
        self.asset = asset
        self.base = base
        self.symbol = asset + base

        self.client = Spot(key=api_key, secret=api_secret)

    def listen(self):
        data =  self.client.klines(symbol=self.symbol,interval="5m",limit=1)
        return {"symbol":self.symbol,"close":data[0][4], "date_received": data[0][6]}

    def message_handler(self, message):
        print(message)

    async def main(self):
        while True:
            print(self.listen())
            await asyncio.sleep(5)

# hb=Heartbeat(asset="ETH", base="USDT", api_key=os.environ["API_KEY_BINANCE"],api_secret=os.environ["API_KEY_BINANCE_SECRET"])

# print(hb)
# print(hb.listen())
# hb.main()
