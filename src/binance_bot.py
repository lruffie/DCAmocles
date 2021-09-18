from dotenv import load_dotenv
from binance.spot import Spot
import binance
import os
import json
import time
import asyncio

load_dotenv()

class Bot:
    def __init__(self, level, amount, asset, base, delta, side, api_key, api_secret, api_url):
        self.level = float(level)
        self.amount = float(amount)
        self.asset = asset
        self.base = base
        self.symbol = (asset + base).upper()
        self.side = side.upper()
        self.delta = float(delta) #in percent of current price
        self.client = Spot(base_url=api_url,key=api_key, secret=api_secret)
        self.counter = 0
        info = self.client.exchange_info()

        for pair in info['symbols']:
            if pair['symbol'] == self.symbol :
                self.info = pair
                self.precision = pair['baseAssetPrecision']
                self.tick = float(pair['filters'][0]['tickSize'])


        #disjonction de cas entre sl et buy back au lancement du bot
        if self.side == "SELL":
            price=self.level*(1-self.delta/100)
            price = int(price/self.tick)*self.tick
            price = "{:0.0{}f}".format(price, self.precision)
            stopPrice=price
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="STOP_LOSS_LIMIT", quantity=float(self.amount) ,price=float(price), stopPrice=float(stopPrice),timeInForce='GTC')
            self.order_id=order['orderId']
            self.order=order
            print(order)

        elif self.side == "BUY" :
            price=self.level*(1+self.delta/100)
            price = int(price/self.tick)*self.tick
            price = "{:0.0{}f}".format(price, self.precision)
            stopPrice=price
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="STOP_LOSS_LIMIT", quantity=float(self.amount) ,price=float(price), stopPrice=float(stopPrice),timeInForce='GTC')
            self.order_id=order['orderId']
            self.order=order
            print(order)
        
        else:
            return 'side error'
        

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
            price = int(price/self.tick)*self.tick
            price = "{:0.0{}f}".format(price, self.precision)
            stopPrice=price
            order=self.client.new_order(symbol=self.symbol, side=self.side, type="STOP_LOSS_LIMIT", quantity=float(self.amount) ,price=price, stopPrice=stopPrice,timeInForce='GTC')
            self.order_id=order['orderId']
            self.order=order
            print(order)
            return order

        elif self.side == "SELL":
            price=level*(1-delta/100)
            price = int(price/self.tick)*self.tick
            price = "{:0.0{}f}".format(price, self.precision)
            stopPrice=price
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

    def track_all_open_orders(self):
        "get status of all open Orders (USER_DATA)"
        order= self.client.get_open_orders()
        return order

    def cancel_order(self):
        print("cancel specific order")
        cancel=self.client.cancel_order(symbol=self.symbol, orderId=self.order_id)
        print(cancel)
        self.order = cancel
        self.order_id = cancel['orderId']        
        return cancel

    def cancel_all_orders(self):
        "cancel all open orders"
        cancel=self.client.cancel_open_orders(symbol=self.symbol)
        return cancel


    ##### BOT #####
    def checks(self):
        self.counter=0 #on met un counter pour éviter les pbms de retours de l'api
        try :
            order_tracked = self.track_order()
            self.order = order_tracked
        except  binance.error.ClientError as err :
            print(err.error_message)
            if err.error_message == 'Order does not exist.' :
                print('unknow order detected, placing new order')
                order = self.place_order()
                return "unknow order detected, placing new order   " + str(order)

        print('symbol :',order_tracked['symbol'], 'type :', order_tracked['type'], ' price_order:', order_tracked['price'], 'level :', self.level, 'status :', order_tracked['status'], 'side_order :', order_tracked['side'], 'side_bot :',self.side)
        # print('type :', order_tracked['type'], ' price_order:', order_tracked['price'], 'status :', order_tracked['status'], 'side_order :', order_tracked['side'], 'side_bot :',self.side)

        # print(order_tracked['status'])
        price_mkt = self.client.ticker_price(symbol=self.symbol)
        print(price_mkt)
        self.price_mkt = price_mkt['price']
        print('counter :  ', self.symbol, "  ", self.counter)


        ##### IF COUNTER PASSED #####
        if self.counter >= 10: # correspond à environ 1.75%
            new_level = self.level*5
            self.side = "BUY"
            order = self.place_order()
            return "MAX NUMBER OF ITERATION REACHED" + str(order)



        ##### IF ORDER FILLED #####
        if self.side == "SELL" and order_tracked['status'] == 'FILLED' and order_tracked['type'] != 'MARKET':
            self.side = "BUY"
            try :
                order = self.place_order()
                self.counter += 1
                return "Stop Loss filled, placing LIMIT order to buy back for :   " + str(order)
            except binance.error.ClientError as err : 
                print(err.error_message)
                if err.error_message == 'Stop price would trigger immediately.' :
                    print('buy back at market now !')
                    order = self.place_order_market()
                    self.counter += 1
                    return "Stop Loss filled + immediate trigger alert, placing NEW MARKET order to buy back for :   " + str(order)

        if self.side == "BUY" and order_tracked['status'] == 'FILLED' and order_tracked['type'] != 'MARKET':
            self.side = "SELL"
            try :
                order = self.place_order()
                self.counter += 1
                return "Take Profit filled, placing LIMIT order to cut losses  for :   " + str(order)
            except binance.error.ClientError as err : 
                print(err.error_message)
                if err.error_message == 'Stop price would trigger immediately.' :
                    print('sell off at market now !')
                    order = self.place_order_market()
                    self.counter += 1
                    return "Take Profit filled + immediate trigger alert, placing NEW MARKET order to cut losses  for :   " + str(order)
           


        ############### IF ORDER PARTIALLY FILLED ###############
        if self.side == "SELL" and order_tracked['status'] == 'PARTIALLY_FILLED' and order_tracked['type'] != 'MARKET':
            amount_left = float(self.amount) - float(order_tracked['executedQty']) 
            print(amount_left)
            amount_left = round(amount_left,self.precision)
            print(amount_left)
            order = self.place_order_market_partial(amount=amount_left)
            self.side = "BUY"
            return "Stop Loss partially filled, placing NEW MARKET order to buy back!   for :   " + str(order)

        if self.side == "BUY" and order_tracked['status'] == 'PARTIALLY_FILLED' and order_tracked['type'] != 'MARKET':
            amount_left = float(self.amount) - float(order_tracked['executedQty']) 
            print(amount_left)
            amount_left = round(amount_left,self.precision)
            print(amount_left)
            order = self.place_order_market_partial(amount=amount_left)
            self.side = "SELL"
            return "Take Profit partially filled, placing NEW MARKET order to cut losses!   for :   " + str(order)






        ############### IF ORDER CANCELED ###############
        if order_tracked['status'] == 'CANCELED':
            order = self.place_order()
            return "Previous order canceled, placing new order   " + str(order)
                




        ############### USER UPDATES ###############

        # action for level and delta update
        level = float(self.level)
        delta = float(self.delta)

        if self.side == "SELL" :
            if float(order_tracked['price']) >= int(level*(1-delta/100)*1.001/self.tick)*self.tick or float(order_tracked['price']) <= int(level*(1-delta/100)*0.999/self.tick)*self.tick:
                print('sell_level_or_delta_update')
                if order_tracked['type'] == 'MARKET':
                    try :
                        order = self.place_order()
                        return "Past order was market buy, new limit order for :   " + str(order)
                    except binance.error.ClientError as err : 
                        print(err.error_code)
                        print(err.error_message)
                        if err.error_message == 'Stop price would trigger immediately.' :
                            print('sell off at market now !')
                            order=self.place_order_market()
                            print(self.side)
                            return "Sell at Market now for :   " + str(order)
                else :
                    try :
                        try :
                            self.cancel_order()
                        except binance.error.ClientError as err : 
                            pass
                        order = self.place_order()
                    except binance.error.ClientError as err : 
                        print(err.error_message)
                        if err.error_message == 'Stop price would trigger immediately.' :
                            try :
                                self.side = "BUY"
                                order = self.place_order()
                                return "Sucessful UPDATE of orders with SIDE CHANGED, past order canceled and new order :   " + str(order)
                            except binance.error.ClientError as err :
                                self.side = "SELL"
                                return "Unsucessful order UPDATE of SIDE, try again :"

                
                    return "Sucessful UPDATE of orders, past order canceled and new order :   " + str(order)

        if self.side == "BUY" :
            if float(order_tracked['price']) >= (self.level*(1+self.delta/100)*1.001/self.tick)*self.tick or float(order_tracked['price']) <= int(self.level*(1+self.delta/100)*0.999/self.tick)*self.tick:
                print('buy_level_or_delta_update')
                if order_tracked['type'] == 'MARKET':
                    try :
                        order = self.place_order()
                        return "Past order was market sell, new limit order for :    " + str(order)
                    except binance.error.ClientError as err : 
                        print(err.error_code)
                        print(err.error_message)
                        if err.error_message == 'Stop price would trigger immediately.' :
                            print('buy back at market now !')
                            order=self.place_order_market()
                            print(self.side)
                            return "Buy at Market now for :   " + str(order)
                        
                else :
                    try :
                        try :
                            self.cancel_order()
                        except binance.error.ClientError as err : 
                            pass
                        order = self.place_order()
                    except binance.error.ClientError as err : 
                        print(err.error_message)
                        if err.error_message == 'Stop price would trigger immediately.' :
                            try :
                                self.side = "SELL"
                                order = self.place_order()
                                return "Sucessful UPDATE of orders with SIDE CHANGED, past order canceled and new order :   " + str(order)
                            except binance.error.ClientError as err :
                                self.side = "BUY"
                                return "Unsucessful order UPDATE of SIDE, try again :"
                
                    return "Sucessful UPDATE of orders, past order canceled and new order :   " + str(order)



        # action for amount update 
        if float(order_tracked['origQty']) >= self.amount*1.001 or float(order_tracked['origQty']) <= self.amount*0.999:
            print('amount_update')
            if order_tracked['type'] == 'MARKET':
                    order = self.place_order()
                    return ("Sucessful update of amounts, new order :", str(order)) 
            else :
                self.cancel_order()
                order = self.place_order()
                return ("Sucessful update of amounts, new order :", str(order)) 

