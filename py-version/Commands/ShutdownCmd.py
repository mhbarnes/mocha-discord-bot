import BotInit as pb
import Commands.HelpCommand as hc
import sys

def cmd_shutdown():
    """
    Shuts down the bot from within the server. Prints shutdown
    message to channel the command was called in, then prints "Bot Closed" in
    the terminal window the bot is running in. Can be performed by any member 
    with admin or higher permissions.

    Usage:
        !shutdown
    """

     # Enable the help message
    hc.enabled_cmds['shutdown'] = True

    @pb.bot.command()
    @pb.commands.has_permissions(administrator=True)
    async def shutdown(ctx):
        await ctx.message.delete()

        # Notifiies the channel that the bot is shutting down
        try:
            await ctx.send(f'Shutting down bot...')
            await pb.bot.close()
        except:
            print("Exception caught: ", sys.exc_info()[0])
            print('Bot Closed')
    return