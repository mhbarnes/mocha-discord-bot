import bot.botinit as mybot
from random import randint

HEADS = 0
TAILS = 1
HEADS_EMOJI = ":regional_indicator_h:"
TAILS_EMOJI = ":regional_indicator_t:"
MAX_COINS = 100

format = lambda x: f"{HEADS_EMOJI} Heads" if x == HEADS else f"{TAILS_EMOJI} Tails"


@mybot.bot.slash_command(
    name="cointoss",
    description="Flips a coin.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="number of coins", 
    description=f"Specifies the number of coins to be flipped, up to {MAX_COINS}. Defaults to 1.",
    required=False,
)
async def cointoss(ctx: mybot.discord.ApplicationContext, num_coins: int = 1):
    """
    Usage:
        /cointoss <num_coins>
    """
    if num_coins < 1 or num_coins > MAX_COINS:
        await ctx.respond("Invalid number of coins.", ephemeral=True)
        return
    embed = mybot.discord.Embed(
        title = "✨**Wheel Spinner Wins**✨",
        color = mybot.discord.Color.dark_gold()
    )
    coin_tosses = [randint(HEADS, TAILS) for x in range(num_coins)]
    
    if num_coins == 1:
        embed.description = format(coin_tosses[0])
        await ctx.respond(embed=embed)
        return
    field = ""
    num_heads = 0
    num_tails = 0
    for i in range(0, num_coins):
        coin = format(coin_tosses[i])
        field += f"{i + 1}. {coin}\n"
        if coin_tosses[i] == HEADS:
            num_heads += 1
        else:
            num_tails += 1
    embed.description = f"**Heads:** {num_heads}, **Tails:** {num_tails}\n"
    embed.add_field(name="Results", value=field)
    await ctx.respond(embed=embed)