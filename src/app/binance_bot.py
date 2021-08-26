from dotenv import load_dotenv
from binance.spot import Spot
import binance
import os
import json
import time
import asyncio

load_dotenv()
class Bot:
    def __init__(self, level, amount, asset, base, side, delta, api_key, api_secret):
        self.level = float(level)
        self.amount = amount
        self.asset = asset
        self.base = base
        self.symbol = (asset + base).upper()
        self.side = side
        self.delta = float(delta) #in percent of current price
        self.client = Spot(base_url='https://testnet.binance.vision',key=api_key, secret=api_secret)
        info = self.client.exchange_info()

        for pair in info['symbols']:
            if pair['symbol'] == self.symbol :
                self.info = pair
                self.precision = pair['baseAssetPrecision']

        # place first order :
        price=self.level*(1-self.delta/100)
        price = "{:0.0{}f}".format(price, self.precision)
        stopPrice=price
        order=self.client.new_order(symbol=self.symbol, side=self.side, type="STOP_LOSS_LIMIT", quantity=float(self.amount) ,price=float(price), stopPrice=float(stopPrice),timeInForce='GTC')
        self.order_id=order['orderId']
        print(order)


    ##### UPDATES #####
    def update_level(self, new_level):
        self.level = new_level
        return "New level set"

    def update_side(self, new_side):
        self.level = new_side
        return "New side set"

    def return_variables(self):
        return self.symbol, self.level, self.side, self.delta

    ##### ACCOUNT DATA #####
    def check_balance(self):
        try :
            data=self.client.account_snapshot("SPOT")
            list=data["snapshotVos"][0]["data"]["balances"]
            for i in range(0,len(list)):
                if list[i]["asset"] == self.asset:
                    self.free_amount = list[i]["free"]
                    self.locked_amount = list[i]["locked"]
            return {"free": self.free_amount, "locked": self.locked_amount}
        except Exception as error:
            return error


    ##### ORDERS #####
    def place_order(self):
        print("placing new order")
        print(self.client.ticker_price(self.symbol))
        level = float(self.level)
        delta = float(self.delta)

        if self.side == "BUY":
            price=level*(1+delta/100)
            price = "{:0.0{}f}".format(price, self.precision)
            stopPrice=price
            # print(price)
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="STOP_LOSS_LIMIT", quantity=float(self.amount) ,price=price, stopPrice=stopPrice,timeInForce='GTC')
            self.order_id=order['orderId']
            self.order=order
            print(order)
            return order

        elif self.side == "SELL":
            price=level*(1-delta/100)
            price = "{:0.0{}f}".format(price, self.precision)
            stopPrice=price
            # print(price)
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="STOP_LOSS_LIMIT", quantity=float(self.amount) ,price=price, stopPrice=stopPrice,timeInForce='GTC')
            self.order_id=order['orderId']
            self.order=order
            print(order)
            return order


    def place_order_market(self):
        print("placing new market order")
        print(self.client.ticker_price(self.symbol))
        print(self.side, self.level)

        if self.side == "BUY":
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="MARKET", quantity=float(self.amount))
            self.order_id=order['orderId']
            self.order=order
            print(order)
            self.side = "SELL"
            return order

        elif self.side == "SELL":
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="MARKET", quantity=float(self.amount))
            self.order_id=order['orderId']
            self.order=order
            print(order)
            self.side = "BUY"
            return order

        
    def place_order_market_partial(self, amount):
        print("placing new market order")
        print(self.client.ticker_price(self.symbol))
        print(self.side, self.level)

        if self.side == "BUY":
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="MARKET", quantity=float(amount))
            self.order_id=order['orderId']
            self.order=order
            print(order)
            self.side = "SELL"
            return order

        elif self.side == "SELL":
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="MARKET", quantity=float(amount))
            self.order_id=order['orderId']
            self.order=order
            print(order)
            self.side = "BUY"
            return order

    def track_order(self):
        "get status of specific order"
        order=self.client.get_order(symbol=self.symbol, orderId=self.order_id)
        # print(order)
        return order
       
    def track_all_orders(self):
        "get status of all open Orders (USER_DATA)"
        order= self.client.get_orders(symbol=self.symbol)
        return order

    def track_all_all_orders(self):
        "get status of all open Orders (USER_DATA)"
        order= self.client.get_open_orders()
        return order

    def cancel_order(self):
        print("cancel specific order")
        cancel=self.client.cancel_order(symbol=self.symbol, orderId=self.order_id)
        print(cancel)
        return cancel

    def cancel_all_orders(self):
        "cancel all open orders"
        cancel=self.client.cancel_open_orders(symbol=self.symbol)
        return cancel


    ##### BOT #####
    def checks(self):
        self.counter=0 #on met un counter pour éviter les pbms de retours de l'api
        order_tracked = self.track_order()
        self.order = order_tracked

        print('symbol :',order_tracked['symbol'], 'type :', order_tracked['type'], ' price_order:', order_tracked['price'], 'level :', self.level, 'status :', order_tracked['status'], 'side_order :', order_tracked['side'], 'side_bot :',self.side)
        # print('type :', order_tracked['type'], ' price_order:', order_tracked['price'], 'status :', order_tracked['status'], 'side_order :', order_tracked['side'], 'side_bot :',self.side)

        # print(order_tracked['status'])
        print(self.client.ticker_price(symbol=self.symbol))

        ##### IF ORDER FILLED #####
        if self.side == "SELL" and order_tracked['status'] == 'FILLED' and order_tracked['type'] != 'MARKET':
            self.side = "BUY"
            try :
                order = self.place_order()
            except binance.error.ClientError as err : 
                print(err.error_message)
                if err.error_message == 'Stop price would trigger immediately.' :
                    print('buy back at market now !')
                    order = self.place_order_market()
            return "Stop Loss filled, placing new order to buy back!" + str(order)

        if self.side == "BUY" and order_tracked['status'] == 'FILLED' and order_tracked['type'] != 'MARKET':
            self.side = "SELL"
            try :
                order = self.place_order()
            except binance.error.ClientError as err : 
                print(err.error_message)
                if err.error_message == 'Stop price would trigger immediately.' :
                    print('sell off at market now !')
                    order = self.place_order_market()
            return "Take Profit filled, placing new order to cut losses!" + str(order)
           


        ##### IF ORDER PARTIALLY FILLED #####
        if self.side == "SELL" and order_tracked['status'] == 'PARTIALLY_FILLED' and order_tracked['type'] != 'MARKET':
            amount_left = order_tracked['executedQty'] - self.amount 
            order = self.place_order_market_partial(amount=amount_left)
            self.side = "BUY"
            return "Stop Loss partially filled, placing new market order to buy back!" + str(order)

        if self.side == "BUY" and order_tracked['status'] == 'PARTIALLY_FILLED' and order_tracked['type'] != 'MARKET':
            amount_left = order_tracked['executedQty'] - self.amount 
            order = self.place_order_market_partial(amount=amount_left)
            self.side = "SELL"
            return "Take Profit partially filled, placing new market order to cut losses!" + str(order) 



        ##### IF ORDER CANCELED #####
        if order_tracked['status'] == 'CANCELED':
                self.place_order()
                

        ### USER UPDATES ###
        # action for level update
        level = float(self.level)
        delta = float(self.delta)
        if self.side == "SELL" :
            if float(order_tracked['price']) >= level*(1-delta/100)*1.0001 or float(order_tracked['price']) <= level*(1-delta/100)*0.9999:
                print('sell_level_or_delta_update')
                if order_tracked['type'] == 'MARKET':
                    try :
                        order = self.place_order()
                    except binance.error.ClientError as err : 
                        print(err.error_code)
                        print(err.error_message)
                        if err.error_message == 'Stop price would trigger immediately.' :
                            print('sell off at market now !')
                            order=self.place_order_market()
                            print(self.side)
                        return "Sucessful update of orders with change side, new order :" + str(order)
                else :
                    self.cancel_order()
                    order = self.place_order()
                    return "Sucessful update of orders, new order :" + str(order) 

            
        if self.side == "BUY" :
            if float(order_tracked['price']) >= self.level*(1+self.delta/100)*1.0001 or float(order_tracked['price']) <= self.level*(1+self.delta/100)*0.9999:
                print('buy_level_or_delta_update')
                if order_tracked['type'] == 'MARKET':
                    try :
                        order = self.place_order()
                    except binance.error.ClientError as err : 
                        print(err.error_code)
                        print(err.error_message)
                        if err.error_message == 'Stop price would trigger immediately.' :
                            print('buy back at market now !')
                            order=self.place_order_market()
                            print(self.side)
                        return "Sucessful update of orders with change side, new order :" + str(order)
                else :
                    self.cancel_order()
                    order = self.place_order()
                    return "Sucessful update of orders, new order :" + str(order)



        # action for amount update 
        if float(order_tracked['origQty']) >= self.amount*1.001 or float(order_tracked['origQty']) <= self.amount*0.999:
            print('amount_update')
            if order_tracked['type'] == 'MARKET':
                    order = self.place_order()
                    return ("Sucessful update of amounts, new order :", order) 
            else :
                self.cancel_order()
                order = self.place_order()
                return ("Sucessful update of amounts, new order :", order) 











        #  # action for delta update 
        # if self.side == "SELL" : 
        #     if float(order_tracked['price']) >= level*(1-delta/100)*1.01 or float(order_tracked['price']) <= level*(1-delta/100)*0.99 :
        #         print('sell_delta_update')
        #         self.cancel_order()
        #         self.place_order()

        # if self.side == "BUY" : 
        #     if float(order_tracked['price']) >= level*(1+delta/100)*1.01 or float(order_tracked['price']) <= level*(1+delta/100)*0.99 :
        #         print('buy_delta_update')
        #         self.cancel_order()
        #         self.place_order()


            # if self.side == "BUY": #that means that we want to "buy back" to re-enter
            #     if price <= self.level :
            #         "do something"

            # if self.side == "SELL": #that means that we want to "sell" to exit
            #     if price <= self.level :
            #         "do something"


# bot=Bot(level=3300,asset="ETH", base="USDT", side="BUY", api_key=os.environ["API_KEY_BINANCE"],api_secret=os.environ["API_KEY_BINANCE_SECRET"])
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