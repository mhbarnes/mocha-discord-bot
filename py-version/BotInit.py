import discord
from discord.ext import commands
from dotenv import load_dotenv          # For loading token and channel IDs
import os                               # "


# Load environment variables
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

TOKEN = os.getenv('TOKEN')                              # Token ID for Bot
MY_GUILD = int(os.getenv('MY_GUILD'))                   # Guild ID
SERVER_ADMIN = os.getenv('SERVER_ADMIN')                # Username of the server admin
EVERYONE = int(os.getenv('EVERYONE'))                   # Role ID for @everyone
POPTROPICANS = int(os.getenv('POPTROPICANS'))           # Role ID for Role1
NOT_POPTROPICANS = int(os.getenv('NOT_POPTROPICANS'))   # Role ID for Bot Role

# Initialize Discord api
#client = discord.Client()

# Initalize Discord bot api
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')