import pickle

from dotenv.main import load_dotenv
import telegram_bot
import dotenv
load_dotenv()
import os
import asyncio

API_KEY_BOT=os.environ['API_KEY_BOT']

favorite_color = { "lion": "yellow", "kitty": "hello" }
favorite_animal = "not skane"
sn=telegram_bot.Snitch(API_KEY_BOT)

file_handler =  open( "store.pkl", "rb" )
# list = [favorite_animal, favorite_color]

# pickle.dump( {'color':favorite_color, 'animal':favorite_animal, 'bot':sn}, file_handler )

list = pickle.load( file_handler )

for w in list :
    print(list[w], type(list[w]))
    if type(list[w]) == dict:
        print('yeet')



# asyncio.run(list[2].main())
# favorite_color = pickle.load( open( "save.p", "rb" ) )


# favorite_color is now { "lion": "yellow", "kitty": "red" }