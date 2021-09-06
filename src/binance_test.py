import requests as req
from dotenv import load_dotenv
from binance.spot import Spot
import os
import json


## client set up ##
load_dotenv()
client = Spot(key=os.environ["API_KEY_BINANCE"], secret=os.environ["API_KEY_BINANCE_SECRET"])

client.account()

## functions ##


def get_balance():
    x=client.account_snapshot("SPOT")
    list=x["snapshotVos"][0]["data"]["balances"]
    print(list)
    return parser_not_null(list)

def parser_not_null(list):
    dict={}
    for idx in range(0,len(list)):
        if float(list[idx]["free"])>1e-9:
            dict.update({list[idx]["asset"]:list[idx]["free"]})
        
    return dict


# print(get_balance())

print(client.book_ticker("BNBUSDT"))
print(client.kline("BNBUSDT","1m"))