from warnings import catch_warnings
from dotenv import load_dotenv
from datetime import datetime
from telegram.ext import *
import os
import binance_test 

load_dotenv()

API_KEY_BOT=os.environ['API_KEY_BOT']

print("bot started ...")
assets=["BTC","ETH","ETC","1INCH","THETA","LINK"]
functions=["balance", "price","setbar"]


def sample_responses(input_text):
    user_message=str(input_text).lower().split()
    print(user_message)

    if user_message in ('hello', 'bitcoin'):
        return "Hey !"

    for i in range(0,len(user_message)-1) :
        for f in functions :
            for a in assets :
                if f=="balance" and a.lower()==user_message[i+1]:
                    try : 
                        data=binance_test.get_balance()[a]
                        return "You have "+ data + a.upper()

                    except err:
                        return err

    else :
        return  "Caca"

def start_command(update, context):
    update.message.reply_text('hello start')

def handle_message(update,context):
    text=str(update.message.text).lower()
    response = sample_responses(text)
    update.message.reply_text(response)

def error(update, context):
    print('error')

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    updater = Updater(API_KEY_BOT)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

main()
