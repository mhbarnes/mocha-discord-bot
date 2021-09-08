#!/usr/bin/python

"""
File: PopBot.py
Author: Michael Barnes
Last Modified: 09/07/2021
Description: Script for a Discord bot that contains various commands.
"""

########################################
# Libraries/Files
########################################
import BotInit as pb
import Commands.HelpCommand as hc
import Commands.PopnameCommand as pnc
import Commands.ShutdownCmd as sdc
import Commands.ReplyCommand as rc
import Commands.PastaCommand as pac
#import Commands.LeaguecheckCommand as lcc



########################################
# MAIN
########################################
def main():
    # Retrieve JSONs
    print('Importing JSON files...')
    pnc.get_popnames()
    rc.get_replies()
    pac.get_pastas()
    hc.get_helpmsgs()
    print('Loaded JSON files.')

    # Initialize commands
    print('Initializing commands...')
    pnc.cmd_popname()
    sdc.cmd_shutdown()
#    cmd_leaguecheck()
    rc.cmd_reply()
    pac.cmd_pasta()
    hc.cmd_help()
    print('Loaded commands.')

    # Enable the bot
    print('Starting Bot...')
    pb.bot.run(pb.TOKEN)
    return



if __name__ == "__main__":    
    main()
