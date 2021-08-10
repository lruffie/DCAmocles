from dotenv import load_dotenv
from binance.spot import Spot
import os
import json


load_dotenv()


class Bot:
    def __init__(self, level, asset, base, side, api_key, api_secret):
        self.level = level
        self.asset = asset
        self.base = base
        self.symbol = asset + base
        self.side = side
        self.client = Spot(key=api_key, secret=api_secret)


    def update_level(self, new_level):
        self.level = new_level
        return "New level set"

    def update_side(self, new_side):
        self.level = new_side
        return "New side set"


    def get_balance(self):
        try :
            data=self.client.account_snapshot("SPOT")
            list=data["snapshotVos"][0]["data"]["balances"]
            for i in range(0,len(list)):
                if list[i]["asset"] == self.asset:
                    self.free_amount = list[i]["free"]
                    self.locked_amount = list[i]["locked"]
            return {"free": self.free_amount, "locked": self.locked_amount}

        except :
            return "error"

    def place_order(self):
        print("placing new order")
        order=self.client.new_order(symbol=self.symbol, side=self.side, type="STOP_LOSS_LIMIT", quantity=0.01 ,price=self.level, stopPrice=self.level,timeInForce='GTC')
        return order

    def track_order(self):
        "get status of order Query Order (USER_DATA)"
        return "something"


    def comparison(self, price):
        if self.side == "BUY":
            if price <= self.level :
                "do something"

        if self.side == "SELL":
            if price <= self.level :
                "do something"

    

bot=Bot(level=3300,asset="ETH", base="USDT", side="BUY", api_key=os.environ["API_KEY_BINANCE"],api_secret=os.environ["API_KEY_BINANCE_SECRET"])
print(bot.get_balance())
print(bot.place_order())

