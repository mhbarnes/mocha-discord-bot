import botinit as pb
import sys

@pb.bot.slash_command(
    name = "shutdown",
    description = "Shuts down the bot from within the server. Must be owner.",
    guild_ids = [pb.MY_GUILD]
)
@pb.discord.default_permissions(administrator=True)
async def shutdown(ctx: pb.discord.ApplicationContext):
    """
    Shuts down the bot from within the server. Prints shutdown
    message to channel the command was called in, then prints "Bot Closed" in
    the terminal window the bot is running in. Can be performed by any member 
    with admin or higher permissions.

    Usage:
        /shutdown
    """
    try:
        await ctx.respond(f'Shutting down bot...')
        await pb.bot.close()
    except:
        print("Exception caught: ", sys.exc_info()[0])
        print('Bot Closed')
