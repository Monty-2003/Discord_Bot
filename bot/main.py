from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# load token from env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# BOT SETUP
intents : Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Handle recieving and sending of messages from bot to user
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty')
        return
    
    # check to see if private message is needed (using '?' command)
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    
    # get response from responses.py and send to private thread or channel
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


    

