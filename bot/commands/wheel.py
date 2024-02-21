import bot.botinit as mybot
from collections import OrderedDict
from random import choices
from os import path
import json


WEIGHTS_MULTIPLIER = 0.1    # Multiplier subtracted depending on number of wins
WINS_FILE = "./bot/resources/wins.json"
member_wins = OrderedDict()
wheel_choices = OrderedDict()

wheel = mybot.bot.create_group("wheel", description="Commands for spinning the wheel.",
                               guild_ids=[mybot.GUILD_ID])
# TODO: change to subgroup after fixed in py-cord
# wins = wheel.create_subgroup("wins", description="Commands for probability weights.",
#                              guild_ids=[mybot.GUILD_ID])
wins = mybot.bot.create_group("wins", description="Commands for wheel probability weights.",
                             guild_ids=[mybot.GUILD_ID])

if path.exists(WINS_FILE):
    try:
        with open(WINS_FILE, "r", encoding = "utf-8") as myJson:
            member_wins = json.load(myJson)
    except:
        print(f"Unable to import file {WINS_FILE}.")


def export_wins():
    with open(WINS_FILE, "w+", encoding = "utf-8") as outfile:
        json.dump(member_wins, outfile, indent=4)


@wheel.command(
    name="add",
    description="Adds a member and choice combination to the wheel options.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="member",
    description="The member associated with the choice.",
    required=True
)
@mybot.option(
    name="choice",
    description="The choice associated with the member.",
    required=True
)
async def add(ctx: mybot.discord.ApplicationContext, 
              member: mybot.discord.Member, choice: str):
    """
    Adds a member and their associated choice to the wheel options.

    Usage:
        /wheel add <@member> <choice>
    """
    if member in wheel_choices.keys():
        msg = f"Changed {member.mention} choice from \"{wheel_choices[member]}\" to \"{choice}\"."
    else: 
        msg = f"Added \"{choice}\" from {member.mention} to the wheel."
    wheel_choices[member] = choice
    await ctx.respond(msg)
    

@wheel.command(
    name="clear",
    description="Clears all current choices in wheel or specific member's choice if specified.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="member",
    description="The member associated with the choice.",
    required=False
)
async def clear(ctx:mybot.discord.ApplicationContext, member: mybot.discord.Member = None):
    """
    Removes a given member and their choice if member is specified. Otherwise, clears all
    members and choices from the wheel.

    Usage:
        /wheel clear <@member>
    """
    if member is None:
        wheel_choices.clear()
        await ctx.respond("Wheel choices cleared.")
        return
    val = wheel_choices.pop(member, None)
    if val is None:
        msg = f"{member.mention} is not in the wheel."
    else:
        msg = f"Removed \"{val}\" by {member.mention} from the wheel."
    await ctx.respond(msg)


@wheel.command(
    name="view",
    description="Shows the current members and choices on the wheel.",
    guild_ids=[mybot.GUILD_ID]
)
async def wheel_view(ctx: mybot.discord.ApplicationContext):
    """
    Usage:
        /wheel view
    """
    msg = "✨**Current Wheel Spinner**✨\n"
    for member, choice in wheel_choices.items():
        msg += f"{member.mention}: {choice}\n"
    await ctx.respond(msg, ephemeral=True)


@wheel.command(
    name="spin",
    description="Spins a weighted wheel, with the options from specified members.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="clear",
    description="Specifies if current wheel choices are cleared after spinning.",
    required=False,
)
async def spin(ctx: mybot.discord.ApplicationContext, clear: bool = True):
    """
    Chooses a weighted random choice from current wheel options and prints the
    winner. A member's chances of winning the next spin decrease on a win, and
    increase on a loss. If clear set to False, the wheel options will be 
    retained

    Usage:
        /wheel spin <clear>
    """
    num_members = len(wheel_choices)
    if num_members == 0:
        await ctx.respond("Cannot spin wheel with no choices.", ephemeral=True)
        return
    adjusted_weights = [100 / num_members] * num_members

    # Decreases odds for past wins, increases odds for past losses
    idx = 0
    for member in wheel_choices.keys():
        if member.id in member_wins.keys():
            adjusted_weights[idx] *= 1 - (member_wins[member.id] * WEIGHTS_MULTIPLIER)
        idx += 1
    print(adjusted_weights)
    result = choices(list(wheel_choices.keys()), weights=adjusted_weights)
    winner = result[0]
    winner_choice = wheel_choices[winner]

    # Update member win record
    for member in wheel_choices.keys():
        if member.id is winner.id:
            if member.id in member_wins.keys():
                member_wins[member.id] = 0 if member_wins[member.id] < 0 else member_wins[member.id] + 1
            else:
                member_wins[member.id] = 1
        elif member.id in member_wins.keys():
            member_wins[member.id] -= 1
        else:
            member_wins[member.id] = -1
    export_wins()
    
    if clear:
        wheel_choices.clear()
    await ctx.respond(f"The winner is {winner.mention} with \"{winner_choice}\"! Congratulations!")


@wins.command(
    name="reset",
    description="Resets the number of wins for all past wheel spins. Must be administrator.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.discord.default_permissions(administrator=True)
async def reset(ctx: mybot.discord.ApplicationContext):
    """
    Usage:
        /wins reset
    """
    for member in member_wins.keys():
        member_wins[member] = 0
    export_wins()
    await ctx.respond(f"All wins reset to 0.", ephemeral=True)


@wins.command(
    name="view",
    description="Shows the current number of wins for all past wheel spin members.",
    guild_ids=[mybot.GUILD_ID]
)
async def wins_view(ctx: mybot.discord.ApplicationContext):
    """
    Requires server members intent.

    Usage:
        /wins view
    """
    msg = "✨**Wheel Spinner Wins**✨\n"
    for member_id, num_wins in member_wins.items():
        member = ctx.guild.get_member(int(member_id))
        msg += f"{member.mention}: {num_wins}\n"
    await ctx.respond(msg, ephemeral=True)