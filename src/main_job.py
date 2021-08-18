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
pickle_file='store.pkl'

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
    
    if x in BotDict.keys() :
        return True
    else :
        return False

def get_bots():
    global BotDict
    list=[]
    for key, value in BotDict.items():
        list.append([key, value.level, value.amount, value.side, value. delta])
    return list

def create_bot(level, asset, base, amount, side, delta):
    global BotDict
    global API_KEY_PUBLIC
    global API_KEY_SECRET
    symb = asset + base
    new_bot =  binance_bot.Bot(level=level,asset=asset,  base=base, amount=amount, side=side, delta=delta, api_key=API_KEY_PUBLIC, api_secret=API_KEY_SECRET)

    BotDict.update({str(symb):new_bot})

def update_bot(symb, **kwargs):
    global BotDict
    for key, value in kwargs.items():
        if key == 'level':
            object = BotDict[symb]
            object.level = value
            BotDict.update({str(symb): object})
        elif key == 'amount':
            object = BotDict[symb]
            object.amount = value
            BotDict.update({str(symb): object})
        elif key == 'delta':
            object = BotDict[symb]
            object.delta = value
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
TelBot.create_bot = create_bot
TelBot.update_bot = update_bot
TelBot.delete_bot = delete_bot

async def manage_bots():
    global BotDict
    while True:
        await asyncio.sleep(10)
        print(BotDict)
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
            
            

async def principal(TelBot):
    global BotDict
    await asyncio.gather(
        await TelBot.main(),
        await manage_bots())

asyncio.run(principal(TelBot))
