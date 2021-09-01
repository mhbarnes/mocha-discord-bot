#!/usr/bin/python

"""
File: PopNameGen.py
Author: Michael Barnes
Last Modified: 04/04/2021
Description: Script for Poptropica Name Generator to create a bot that
    contains various commands.
"""

########################################
# Libraries
########################################
import discord                          # For discord api
from discord.ext import commands        # "
from discord.ext.commands import Bot    # "
import json                             # For importing PoptropicaNames.json
import random                           # For generating poptropica name
from dotenv import load_dotenv          # For loading token and channel IDs
import os                               # "


########################################
# Globals
########################################
# File names
names_file = 'PoptropicaNames.json' # JSON containing possible poptropica names
replies_file = 'Replies.json'       # JSON containing replies
helpmsg_file = 'HelpMsg.json'       # JSON containing help messages


# Data structures
poptropica_names = {}   # Dictionary of Poptropica names
replies = {}            # Dictionary of replies and copypastas
help_msgs = {}          # Dictionary of help messages
enabled_cmds = {}       # Dictionary to track enabled commands

# Initialize Discord api
client = discord.Client()

# Initalize Discord bot api
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

# Variables from .env
TOKEN = ''      # Token ID for Bot
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
    # Retrieve JSONs
    get_popnames()
    get_replies()
    get_helpmsgs()

    # Initialize commands
    cmd_popname()
    cmd_shutdown()
#    cmd_leaguecheck()
    cmd_reply()
    cmd_pasta()
    cmd_help()

    # Initialize channel utilities
#    init_oneshot()

    # Enable the bot
    print('Starting Bot...')
    bot.run(TOKEN)
    return


########################################
# Command Definitions
########################################

#-------------------------------------------------------------------------------
# Command: popname
# Usage: !popname @<member>
# Description: Generates a random Poptropica name for @member. Command only
#   works if @member does not have a role yet, EXCEPT if message author has a
#   role higher than POPTROPICANS
#-------------------------------------------------------------------------------
def cmd_popname():
    # Enable the help message
    global enabled_cmds
    enabled_cmds['popname'] = True

    @bot.command()
    async def popname(ctx, member: discord.Member):
        # Retrieve guild ID for accessing server members
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
    return


#-------------------------------------------------------------------------------
# Command: shutdown
# Usage: !shutdown
# Description: Shuts down the bot from within the server. Prints shutdown
#   message to channel the command was called in, then prints "Bot Closed" in
#   the terminal window the bot is running in. Can be performed by any member 
#   with admin or higher permissions.
#-------------------------------------------------------------------------------
def cmd_shutdown():
    # Enable the help message
    global enabled_cmds
    enabled_cmds['shutdown'] = True

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def shutdown(ctx):
        # Notifiies the channel that the bot is shutting down
        await ctx.send(f'Shutting down bot...')
        await ctx.bot.logout()
        print('Bot Closed')
    return


#-------------------------------------------------------------------------------
# Command: leaguecheck
# Usage: !leaguecheck [on, off]
# Description: 
#-------------------------------------------------------------------------------
def cmd_leaguecheck():
    # Enable the help message
    global enabled_cmds
    enabled_cmds['leaguecheck'] = True

    #TODO add argument handling
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def leaguecheck(ctx):
        # Retrieve guild ID for accessing server members
        guild = bot.get_guild(MY_GUILD)
        await ctx.send(f'League check :leg:')
        # TODO iteerate through member list, check if any playing league & in voice chat
    return


#-------------------------------------------------------------------------------
# Command: reply
# Usage: !reply
# Description: Sends a random message to chat from JSON list
#-------------------------------------------------------------------------------
def cmd_reply():
    # Enable the help message
    global enabled_cmds
    enabled_cmds['reply'] = True
    
    @bot.command()
    async def reply(ctx, arg=None):
        # Generate random reply
        msg = random.choice(replies['replies'])
        await ctx.send(msg)
    return


#-------------------------------------------------------------------------------
# Command: pasta
# Usage: !pasta <option>
# Description: Outputs a copypasta. Below are a list of options:
#               ghaul:  "You just never quit do you?..."
#               redwar: "Whether we wanted it or not..."
#              If option is not specified, a random copypasta is used.
#-------------------------------------------------------------------------------
def cmd_pasta():
    # Enable the help message
    global enabled_cmds
    enabled_cmds['pasta'] = True

    @bot.command()
    async def pasta(ctx, arg=None):
        # Convert the copypasta option to lowercase
        option = arg
        if option is None:
            random_key = random.choice(list(replies['copypastas']))
            msg = replies['copypastas'][random_key]
            await ctx.send(msg)
            return
        else:
            option = arg.lower()
        # Process option
        if option == "list":
            msg = ".\n"
            for pasta in sorted(replies['copypastas'].keys()):
                msg += '[' + pasta + ']\n'
        elif option in replies['copypastas'].keys():
            msg = replies['copypastas'][option]
        else:
            return
        await ctx.send(msg)
    return
         

#-------------------------------------------------------------------------------
# Command: help
# Usage: !help
# Description: Lists all available enabled commands in chat.
#-------------------------------------------------------------------------------
def cmd_help():
    # Enable the help message
    global enabled_cmds
    enabled_cmds['help'] = True

    @bot.command()
    async def help(ctx):
        msg = '__**Available commands:**__\n\n'
        for cmd in enabled_cmds:
            if enabled_cmds[cmd] is True:
                msg = msg + help_msgs['helpmsgs'][cmd]['name'] + help_msgs['helpmsgs'][cmd]['msg'] + help_msgs['helpmsgs'][cmd]['usage'] + '\n'
        await ctx.send(msg)
    return



########################################
# Miscellaneous
########################################
# Sets up tracker for channel "one-shot"
def init_oneshot():
    #TODO add role to track people who've sent a message to the channel
    return



########################################
# Helper Functions
########################################
# Grabs list of Poptropica first/last names from PoptropicaNames.json
def get_popnames():
    with open(names_file, 'r') as myJson:
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


# Grabs list of replies and copypastas from Replies.json
def get_replies():
    with open(replies_file, 'r', encoding = 'utf-8') as myJson:
        replies.update(json.load(myJson))
    return


# Grabs list of help messages from HelpMsg.json
def get_helpmsgs():
    with open(helpmsg_file, 'r', encoding = 'utf-8') as myJson:
        help_msgs.update(json.load(myJson)) 
    return



if __name__ == "__main__":
    # Load environment variables
    base_dir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(base_dir, '.env'))
    TOKEN = os.getenv('TOKEN')
    MY_GUILD = int(os.getenv('MY_GUILD'))
    SERVER_ADMIN = os.getenv('SERVER_ADMIN')
    EVERYONE = int(os.getenv('EVERYONE'))
    POPTROPICANS = int(os.getenv('POPTROPICANS'))
    NOT_POPTROPICANS = int(os.getenv('NOT_POPTROPICANS'))
    
    main()
