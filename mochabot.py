#!/usr/bin/python
import bot.botinit as mybot
import bot.config

# Enable the bot
print("Starting Bot...")
try:
    mybot.bot.run(mybot.TOKEN)
except Exception as e:
    print(f"Login unsuccessful. Exception caught: {e}")