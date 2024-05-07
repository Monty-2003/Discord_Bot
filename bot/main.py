from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
#from responses import get_response

# load token from env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

