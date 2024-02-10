from dotenv import load_dotenv          # For loading token and channel IDs
from os import path, getenv
import discord
from discord.ext import commands
from discord.commands import option

# Load environment variables
base_dir = path.abspath(path.dirname(path.dirname(__file__)))
load_dotenv(path.join(base_dir, ".env"))

TOKEN = getenv("TOKEN")                                  # Token ID for bot
GUILD_ID = int(getenv("GUILD_ID"))                       # Guild ID
EVERYONE = int(getenv("EVERYONE"))                       # Role ID for @everyone
MEMBER_ROLE_ID = int(getenv("MEMBER_ROLE_ID"))           # Role ID for members
BOT_ROLE_ID = int(getenv("BOT_ROLE_ID"))                 # Role ID for bot role
MODERATOR = int(getenv("MODERATOR"))                     # Role ID for Moderator Role
GUILD_OWNER_USERNAME = getenv("GUILD_OWNER_USERNAME")    # Username of guild owner

# Initalize Discord bot api
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    """
    Prints to console when bot is ready.
    """
    print(f"Logged in as {bot.user}")


