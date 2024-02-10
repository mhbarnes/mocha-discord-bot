import bot.botinit as mybot

@mybot.bot.slash_command(
    name="imdb",
    description="Fetches movie info from IMDB.",
    guild_ids=[mybot.GUILD_ID]
)
async def imdb(ctx: mybot.discord.ApplicationContext, movie_name: str):
    """
    Description

    Usage:
        /imdb <movie_name>
    """
    
