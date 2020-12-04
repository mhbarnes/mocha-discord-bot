#!/usr/bin/python3

"""
File: PopNameGen.py
Author: Michael Barnes
Last Modified: 10/30/20
Description: Script for Poptropica Name Generator to create a command that
    generates a random Poptropica name
"""

########################################
# Libraries
########################################
import discord                      # For discord api
from discord.ext import commands
from discord.ext.commands import Bot
import json                         # For importing PoptropicaNames.json
import random                       # For generating poptropica name
from dotenv import load_dotenv      # For loading token and channel IDs
import os


########################################
# Globals
########################################
# Dictionary of Poptropica names
poptropica_names = {}


# Initialize Discord api
client = discord.Client()


# Initalize Discord bot api
bot = commands.Bot(command_prefix='!')


# Variables from .env
BOT_TOKEN = ''      # Token ID for Bot
MY_GUILD = 0        # Guild ID
SERVER_ADMIN = ''   # Username of the server admin

# Roles
EVERYONE = 0            # Role ID for @everyone
POPTROPICANS = 0        # Role ID for Role1
NOT_POPTROPICANS = 0    # Role ID for Bot Role



########################################
# MAIN
########################################
def main():
    # Retrieve JSON
    get_popnames()

    # popname command
    @bot.command()
    async def popname(ctx, member: discord.Member):
        guild = bot.get_guild(MY_GUILD)
        if check_role_assigned(guild, member) == True:
            new_nick = gen_popname()
            # Checks if nickname is already in place
            while guild.get_member_named(new_nick) != None:
                new_nick = gen_popname()
            # Update nickname and role
            await member.edit(nick=new_nick)
            await member.add_roles(guild.get_role(POPTROPICANS))
            await ctx.send(f'Henceforth {member.name} will be known as {member.mention}.')
        elif ctx.message.author.top_role > guild.get_role(POPTROPICANS):
            new_nick = gen_popname()
            # Checks if nickname is already in place
            while guild.get_member_named(new_nick) != None:
                new_nick = gen_popname()
            # Update nickname and role
            await member.edit(nick=new_nick)
            await ctx.send(f'Henceforth {member.name} will be known as {member.mention}.')
        else:
            await ctx.send(f'Idiot. {member.mention} has already been assigned a sick role and rad name.')

    # close bot command
    @bot.command(aliases=["quit"])
    @commands.has_permissions(administrator=True)
    async def shutdown(ctx):
        await ctx.bot.logout()
        print('Bot Closed')

    bot.run(BOT_TOKEN)
    return


########################################
# Functions
########################################
# Grabs list of Poptropica first/last names from PoptropicaNames.json
def get_popnames():
    with open('PoptropicaNames.json', 'r') as myJson:
        poptropica_names.update(json.load(myJson))
    return


# Generates random Poptropica name of form 'first last'
def gen_popname():
    new_popname = random.choice(poptropica_names['names']['first']) + ' ' + random.choice(poptropica_names['names']['last'])
    return new_popname


# Checks if the user being mentioned in the command doesn't have a role
def check_role_assigned(g, user):
    if user.top_role == g.get_role(EVERYONE):
        return True
    return False



if __name__ == "__main__":
    # Load environment variables
    base_dir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(base_dir, '.env'))
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    MY_GUILD = int(os.getenv('MY_GUILD'))
    SERVER_ADMIN = os.getenv('SERVER_ADMIN')
    EVERYONE = int(os.getenv('EVERYONE'))
    POPTROPICANS = int(os.getenv('POPTROPICANS'))
    NOT_POPTROPICANS = int(os.getenv('NOT_POPTROPICANS'))
    main()
