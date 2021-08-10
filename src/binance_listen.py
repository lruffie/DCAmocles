from dotenv import load_dotenv
from binance.spot import Spot
import time
import os
import json

load_dotenv()

class Heartbeat:
    def __init__(self, asset, base, side, api_key, api_secret):
        self.asset = asset
        self.base = base
        self.side = side
        self.symbol = asset + base
        self.client = Spot(key=api_key, secret=api_secret)

    def listen(self):

        data = self.client.klines(symbol=self.symbol,interval="5m",limit=1)
        return {"close":data[0][4], "date_received": data[0][6]}

    def message_handler(self, message):
        print(message)

    def main(self):
        while True:
            print(self.listen())
            time.sleep(5)

hb=Heartbeat(asset="ETH", base="USDT", side="BUY", api_key=os.environ["API_KEY_BINANCE"],api_secret=os.environ["API_KEY_BINANCE_SECRET"])

print(hb)
print(hb.listen())
hb.main()
