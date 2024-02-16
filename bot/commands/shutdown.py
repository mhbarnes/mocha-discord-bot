import bot.botinit as mybot

@mybot.bot.slash_command(
    name = "shutdown",
    description = "Shuts down the bot from within the server. Must be administrator.",
    guild_ids = [mybot.GUILD_ID]
)
@mybot.discord.default_permissions(administrator=True)
async def shutdown(ctx: mybot.discord.ApplicationContext):
    """
    Shuts down the bot from within the server. Prints shutdown
    message to channel the command was called in, then prints "Bot Closed" in
    the terminal window the bot is running in. Can be performed by any member 
    with admin or higher permissions.

    Usage:
        /shutdown
    """
    try:
        await ctx.respond(f'Shutting down bot...', ephemeral=True)
        await mybot.bot.close()
    except Exception as e:
        print("Exception caught: ", e)
    finally:
        print('Bot Closed')
