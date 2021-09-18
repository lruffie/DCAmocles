from asyncio.streams import StreamReader
from warnings import catch_warnings
from dotenv import load_dotenv
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import os
import asyncio
import re
import time

load_dotenv()


# ADD @RawDataBot to your group chat to find its id
API_KEY_BOT=os.environ['API_KEY_BOT']

print("bot started ...")
class Snitch :
    def __init__(self, api_key_tel):
        self.api_key=api_key_tel
        self.chat_id='-581022911'
        # self.check_exist = check_exist

    def external_message(self, input):
        self.updater.bot.send_message(chat_id=self.chat_id,text=str(input))

    def handle_message(self, update, context):
            text=str(update.message.text).lower()
            self.updater.bot.send_message(chat_id=self.chat_id,text="Sorry I did not understand your request. Press /help for more info.")

    def start_command(self, update, context):
        self.updater.bot.send_message(chat_id=self.chat_id,text='Hello start, use /help for more info')
        self.updater.bot.send_message('ze parti')

    def help_command(self, update, context):
        self.updater.bot.send_message(chat_id=self.chat_id,text='Use /create to create new bot with syntax : asset:btc_base:usdt_amount:1.0_level:2000.1_delta:0.1_side:sell')
        self.updater.bot.send_message(chat_id=self.chat_id,text='Use /getorders to have all open orders')
        self.updater.bot.send_message(chat_id=self.chat_id,text='Use /update to update bot params with params symb:btcusdt_level:20000.0 or symb:btcusdt_amount:2.0 or symb:btcusdt_delta:0.1')
        self.updater.bot.send_message(chat_id=self.chat_id,text='Use /get to get bot with syntax symb:ethusdt')
        self.updater.bot.send_message(chat_id=self.chat_id,text='Use /delete to delete bot with syntax symb:usdt')
        # self.confirmation(update, context)

    def get_orders_command(self, update, context):
        idx=(str(update.message.text)).find(' ')
        mess=(str(update.message.text))[idx+1:]

        print(mess)
        self.updater.bot.send_message(chat_id=self.chat_id,text='You want to get open orders : ')
        try :
            info=self.get_orders()
            print(info)
            if len(info)==0 :
                self.updater.bot.send_message(chat_id=self.chat_id,text='No open orders !')
            else : 
                for i in info:
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Open order number ' + str(info.index(i) + 1) + "   " + str(i))
        except Exception as err:
            err=str(err)
            self.updater.bot.send_message(chat_id=self.chat_id,text='Error'+err)





    #### MAIN FUNCTIONS ####
    def create_command(self, update, context):
        "add exception raising and check for existing bot and store new bot params and ask for user confirmation"
        idx=(str(update.message.text)).find(' ')
        mess=(str(update.message.text))[idx+1:]
        print(mess)
        regex1 = 'asset:[a-zA-Z]+_base:[a-zA-Z]+_amount:[0-9]*\.[0-9]+_level:[0-9]*\.[0-9]+_delta:[0-9]*\.[0-9]+_side:[a-zA-Z]+'
        regex2 = 'asset:[a-zA-Z]+_base:[a-zA-Z]+_amount:[0-9]*\.[0-9]+_level:[0-9]+_delta:[0-9]*\.[0-9]+_side:[a-zA-Z]+'
        regex3 = 'asset:[a-zA-Z]+_base:[a-zA-Z]+_amount:[0-9]+_level:[0-9]+_delta:[0-9]*\.[0-9]+_side:[a-zA-Z]+'
        regex4 = 'asset:[a-zA-Z]+_base:[a-zA-Z]+_amount:[0-9]+_level:[0-9]*\.[0-9]+_delta:[0-9]*\.[0-9]+_side:[a-zA-Z]+'

        if self.check_expression(regex1, mess, update) or self.check_expression(regex2, mess, update) or self.check_expression(regex3, mess, update) or self.check_expression(regex4, mess, update):
            data=self.tel_parser(mess, ['asset','base','side'])
            symb = str( data['asset'] + data['base'])
            print(symb)
            self.updater.bot.send_message(chat_id=self.chat_id,text='you want to create a bot with these parameters'+' '+str(data))
            if self.check_exist(symb) == False :
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot creation process launched for '+symb)
                try : 
                    create_return = self.create_bot(level=data['level'], 
                                    asset=data['asset'].upper(),
                                    base=data['base'].upper(),
                                    amount=data['amount'],
                                    delta=data['delta'],
                                    side=data['side'])
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Bot succesfully created !')
                    self.updater.bot.send_message(chat_id=self.chat_id,text=str(create_return))
                except Exception as err :
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Error :'+str(err))
            else :
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot already exists please update')
        else : 
            self.updater.bot.send_message(chat_id=self.chat_id,text='Invalid Expression : Check /help section for more info')







    def update_command(self, update, context):
        "add regex control and exception raising and check for bot exists and ask for user confirmation"
        idx=(str(update.message.text)).find(' ')
        mess=(str(update.message.text))[idx+1:]
        print(mess)
        regex_level1= 'symb:[a-zA-Z]+_level:[0-9]*\.[0-9]+'
        regex_amount1= 'symb:[a-zA-Z]+_amount:[0-9]*\.[0-9]+'
        regex_delta1= 'symb:[a-zA-Z]+_delta:[0-9]*\.[0-9]+'
        regex_level2= 'symb:[a-zA-Z]+_level:[0-9]+'
        regex_amount2= 'symb:[a-zA-Z]+_amount:[0-9]+'

        if self.check_expression_bis(regex_level1, mess, update) or self.check_expression_bis(regex_level2, mess, update):
            data=self.tel_parser(mess, ['symb','level'])
            self.updater.bot.send_message(chat_id=self.chat_id,text='you want to update a bot with level parameter'+' '+str(data))
            data['symb'] = data['symb'].upper()

            if self.check_exist(data['symb']) == True :
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot update process launched for '+str(data['symb']))
                try : 
                    self.update_bot(symb=data['symb'] ,level=float(data['level']))
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Bot succesfully updated ! But orders needs to be changed now, wait for confirmation :')
                except Exception as err :
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Error :'+str(err))
            else : 
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot doesnt exist, use /create')

        elif self.check_expression_bis(regex_amount1, mess, update) or self.check_expression_bis(regex_amount2, mess, update):
            data=self.tel_parser(mess, ['symb','amount'])
            self.updater.bot.send_message(chat_id=self.chat_id,text='you want to update a bot with amout parameter'+' '+str(data))
            data['symb'] = data['symb'].upper()

            if self.check_exist(data['symb']) == True :
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot update process launched for '+str(data['symb']))
                try : 
                    self.update_bot(symb=data['symb'] ,amount=float(data['amount']))
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Bot succesfully updated ! But orders needs to be changed now, wait for confirmation :')
                except Exception as err :
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Error :'+str(err))
            else : 
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot doesnt exist, use /create')


        elif self.check_expression_bis(regex_delta1, mess, update):
            data=self.tel_parser(mess, ['symb','delta'])
            self.updater.bot.send_message(chat_id=self.chat_id,text='You want to update a bot with delta parameter'+' '+str(data))
            data['symb'] = data['symb'].upper()

            if self.check_exist(data['symb']) == True :
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot update process launched for '+str(data['symb']))
                try : 
                    self.update_bot(symb=data['symb'] ,delta=float(data['delta']))
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Bot succesfully updated ! But orders needs to be changed now, wait for confirmation :')
                except Exception as err :
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Error :'+str(err))
            else : 
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot doesnt exist, use /create')
        else : 
            self.updater.bot.send_message(chat_id=self.chat_id,text='Invalid Expression : Check /help section for more info')







    def get_command(self, update, context):
        "add exception raising"
        idx=(str(update.message.text)).find(' ')
        mess=(str(update.message.text))[idx+1:]
    
        print(mess)
        self.updater.bot.send_message(chat_id=self.chat_id,text='You want to get existing bots parameters')
        try :
            info=self.get_bots()
            if len(info)==0 :
                self.updater.bot.send_message(chat_id=self.chat_id,text='No bots running !')
            else : 
                for i in info:
                    self.updater.bot.send_message(chat_id=self.chat_id,text='Bot parameters  :  '+ str(i))
        except Exception as err:
            err=str(err)
            self.updater.bot.send_message(chat_id=self.chat_id,text='Error'+err)





    def delete_command(self, update, context):
        "ask for user confirmation"
        regex= 'symb:[a-zA-Z]+'
        idx=(str(update.message.text)).find(' ')
        mess=(str(update.message.text))[idx+1:]
        print(mess)
        if self.check_expression(regex, mess, update):
            data=self.tel_parser(mess, ['symb'])
            print(data)
            data['symb'] = data['symb'].upper()
            self.updater.bot.send_message(chat_id=self.chat_id,text='You want to delete a bot actual params with these parameters'+' '+str(data))
            try :
                delete_return = self.delete_bot(data['symb'])
                self.updater.bot.send_message(chat_id=self.chat_id,text='Bot sucessfully deleted !')
                self.updater.bot.send_message(chat_id=self.chat_id,text=str(delete_return))
            except Exception as err:
                err = str(err)
                self.updater.bot.send_message(chat_id=self.chat_id,text='Error'+err)
        else : 
            self.updater.bot.send_message(chat_id=self.chat_id,text='Invalid Expression : Check /help section for more info')




    def stop_command(self, update, context):
        "add regex control and exception raising and check for bot exists and ask for confirmation"
        self.updater.bot.send_message(chat_id=self.chat_id,text='See you in the next life !')
        self.updater.stop()




    def error(self, update, context):
        print('error')









    #### TOOLS and SPECIFIC FUNCTIONS ####
    def check_expression(self, regex, input, update):
        reg = str(regex)
        if(re.fullmatch(reg, input)):
            print("Valid expression")
            return True
        else:
            return False

    def check_expression_bis(self, regex, input, update):
        reg = str(regex)
        if(re.fullmatch(reg, input)):
            print("Valid expression")
            return True
        else:
            return False

    def tel_parser(self, input, non_numerical):
        f=input.split('_')
        dico={}
        for u in f:
            print(u)
            x=u.split(':')
            if x[0] in non_numerical :
                d={str(x[0]):x[1]}
            else :
                d={str(x[0]):float(x[1])}
            dico.update(d)
        return dico

    # def confirmation(self, update, context):
    #     "add regex control and exception raising and check for bot exists"
    #     self.updater.bot.send_message(chat_id=self.chat_id,text='Are you sure ? (Answer with y or n) you have 10 seconds.')
    #     time.sleep(10)
    #     update=self.updater.bot.getUpdates(timeout=10)
    #     print(update)
    #     if len(update) > 0 :
    #         update=update[0]
    #         print(update)

    #         if  update.message.text == "y": 
    #             self.updater.bot.send_message(chat_id=self.chat_id,text="Ok let's go !")
    #             return True
    #         elif update.message.text == "n":
    #             self.updater.bot.send_message(chat_id=self.chat_id,text="Ok maybe next time !")
    #             return False
    #         else :
    #             return False
    #     else : 
    #         self.updater.bot.send_message(chat_id=self.chat_id,text="Try again")
    # maybe this : http://5.9.10.113/65778527/cant-seem-to-find-a-way-to-make-my-telegram-bot-wait-for-user-input
    # or https://elixirforum.com/t/wait-for-a-response-from-a-user/6016/6

    async def main(self):
        self.updater = Updater(self.api_key)
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start_command))
        self.dp.add_handler(CommandHandler("help", self.help_command))
        self.dp.add_handler(CommandHandler("getorders", self.get_orders_command))
        self.dp.add_handler(CommandHandler("create", self.create_command))
        self.dp.add_handler(CommandHandler("update", self.update_command))
        self.dp.add_handler(CommandHandler("get", self.get_command))
        self.dp.add_handler(CommandHandler("delete", self.delete_command))
        self.dp.add_error_handler(CommandHandler("delete", self.error))
        self.dp.add_handler(MessageHandler(Filters.text, self.handle_message))
        self.dp.add_handler(CommandHandler("stop", self.stop_command))

        self.updater.start_polling(2)
        # await updater.idle()


# BotDict={'ethusdt':{'level':1, 'amount':1, 'base':1, 'asset':1, 'side':1, 'delta':1}}

# def check_exist(x):
#     global BotDict
    
#     if x in BotDict.keys() :
#         return True
#     else :
#         return False


# def get_bots():
#     global BotDict
#     list=[]
#     for key, value in BotDict.items():
#         list.append([key, value.level, value.amount, value.side, value. delta])
#     return list

# def create_bot(level, asset, base, amount, side, delta):
#     global BotDict
#     global API_KEY_PUBLIC
#     global API_KEY_SECRET

#     new_bot =  binance_bot.Bot(level=level,asset=asset,  base=base, amount=amount, side=side, delta=delta, api_key=API_KEY_PUBLIC, api_secret=API_KEY_SECRET)

#     BotDict.update({str(asset):new_bot})

# def update_bot(symb, **kwargs):
#     global BotDict
#     for key, value in kwargs.items():
#         if key == 'level':
#             object = BotDict[symb]
#             object.level = value
#             BotDict.update({str(symb): object})
#         elif key == 'amount':
#             object = BotDict[symb]
#             object.level = value
#             BotDict.update({str(symb): object})
#         elif key == 'delta':
#             object = BotDict[symb]
#             object.level = value
#             BotDict.update({str(symb): object})

#     # actual bot needs to be updated --> orders changed

# def delete_bot(symb):
#     global BotDict
#     BotDict['symb'].cancel_all_orders() 
#     BotDict.pop(symb)

# sn=Snitch(API_KEY_BOT)
# sn.check_exist = check_exist
# sn.get_bots = get_bots 
# # sn.update_bot = update_bot
# # sn.creatte_bot = create_bot
# sn.delete_bot = delete_bot

# async def do_smth():
#     i = 0
#     while True:
#         i+=1
#         print(i)
#         await asyncio.sleep(1)

# async def principal(sn):
#     await asyncio.gather(
#         do_smth(),
#         sn.main(),
#     )

# asyncio.run(principal(sn))

