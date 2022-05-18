#!/usr/bin/python

"""
File: PopBot.py
Author: Michael Barnes
Description: Script for a Discord bot that contains various commands.
"""

########################################
# Libraries/Files
########################################
import botinit as pb
import commands.popname as pnc
import commands.shutdown as sdc
import commands.reply as rc
import commands.pasta as pac
#import commands.leaguecheck as lcc


########################################
# MAIN
########################################
def main():
    # Enable the bot
    print('Starting Bot...')
    pb.bot.run(pb.TOKEN)
    return


if __name__ == "__main__":    
    main()
