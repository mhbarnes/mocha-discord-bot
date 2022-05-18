import discord
from discord.ext import commands
from discord.commands import option
from dotenv import load_dotenv          # For loading token and channel IDs
import os                               # "


# Load environment variables
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

TOKEN = os.getenv('TOKEN')                              # Token ID for Bot
MY_GUILD = int(os.getenv('MY_GUILD'))                   # Guild ID
EVERYONE = int(os.getenv('EVERYONE'))                   # Role ID for @everyone
POPTROPICANS = int(os.getenv('POPTROPICANS'))           # Role ID for Role1
NOT_POPTROPICANS = int(os.getenv('NOT_POPTROPICANS'))   # Role ID for Bot Role
MODERATOR = int(os.getenv('MODERATOR'))                 # Role ID for Moderator Role
SERVER_OWNER = os.getenv('SERVER_OWNER')                # Username of the server owner

# Initalize Discord bot api
bot = discord.Bot(command_prefix="!")
# bot = commands.Bot()

@bot.event
async def on_ready():
    """
    Prints to console when bot is ready.
    """
    print(f"Logged in as {bot.user}")
