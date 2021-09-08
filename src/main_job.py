import telegram_bot
import binance_bot

import pickle
import asyncio
import re
import os
from dotenv import load_dotenv

######################### INIT #########################

load_dotenv()
API_KEY_BOT = os.environ['API_KEY_BOT']
API_KEY_PUBLIC=os.environ["API_KEY_TEST_NET"]
API_KEY_SECRET=os.environ["API_KEY_TEST_NET_SECRET"]

#### LOAD PREVIOUS BOTS ####
path=os.getcwd()
pickle_file=path+'/store.pkl'
print(pickle_file)

### load ###
with open( pickle_file, "rb" ) as file_handler:
    try : 
        BotDict = pickle.load( file_handler )
    except Exception as err :
        print(err)
        BotDict={}

### set for next writes ###

########### INIT TEL BOT #############
def check_exist(x):
    global BotDict
    
    x=x.upper()
    if x in BotDict.keys() :
        return True
    else :
        return False

def get_bots():
    global BotDict
    list=[]
    for key, value in BotDict.items():
        list.append([key, "level :",value.level,  "amount :",value.amount,  "side :",value.side,  "delta :",value.delta, "order_price :",value.order['price']])
    return list

def get_orders():
    global BotDict
    list=[]
    for key, value in BotDict.items(): 
        list.append([key, "order :", value.track_all_open_orders()])
    return list

def create_bot(level, asset, base, amount, side, delta):
    global BotDict
    global API_KEY_PUBLIC
    global API_KEY_SECRET
    symb = asset + base
    new_bot =  binance_bot.Bot(level=level,asset=asset,  base=base, amount=amount, side=side, delta=delta, api_key=API_KEY_PUBLIC, api_secret=API_KEY_SECRET)

    BotDict.update({str(symb):new_bot})
    return new_bot

def update_bot(symb, **kwargs):
    global BotDict
    for key, value in kwargs.items():
        if key == 'level':
            object = BotDict[symb]
            object.level = float(value)
            BotDict.update({str(symb): object})
        elif key == 'amount':
            object = BotDict[symb]
            object.amount = float(value)
            BotDict.update({str(symb): object})
        elif key == 'delta':
            object = BotDict[symb]
            object.delta = float(value)
            BotDict.update({str(symb): object})

    # actual bot needs to be updated --> orders changed

def delete_bot(symb):
    global BotDict
    if BotDict[symb].order != 'MARKET' :
        cancel = BotDict[symb].cancel_all_orders() 
    BotDict.pop(symb)
    return cancel

    # actual bot needs to be updated --> orders cancelled

TelBot=telegram_bot.Snitch(API_KEY_BOT)
TelBot.check_exist = check_exist
TelBot.get_bots = get_bots
TelBot.get_orders = get_orders
TelBot.create_bot = create_bot
TelBot.update_bot = update_bot
TelBot.delete_bot = delete_bot

async def manage_bots():
    global BotDict
    while True:
        await asyncio.sleep(10)
        print('---------------------------------------')
        # print(BotDict)
        with open( pickle_file, "wb" ) as file_handler:
            pickle.dump(BotDict, file_handler)

        #### add try except because this async function stops if one error raised
        try : 
            for key in BotDict.keys(): 
                response = BotDict[key].checks()
                if response != None:
                    TelBot.external_message(str(response))
        except Exception as err : 
            print(err)
            TelBot.external_message(str(err))
            
async def pinger():
    "create ping function to send message after x time, then if ping not received force reboot of script"

async def principal(TelBot):
    global BotDict
    await asyncio.gather(
        await TelBot.main(),
        await manage_bots())

asyncio.run(principal(TelBot))
