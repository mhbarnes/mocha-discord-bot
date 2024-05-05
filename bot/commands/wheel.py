import bot.botinit as mybot
from random import choices
import os
from dataclasses import dataclass
from typing import Dict
import yaml

@dataclass
class Record:
    weight: int = 0
    wins: int = 0
    losses: int = 0

    # For clean YAML export
    yaml_tag = "!record"
    @staticmethod
    def to_yaml(dumper: yaml.SafeDumper, data):
        node = dumper.represent_mapping(Record.yaml_tag, 
                                        {"weight": data.weight,
                                         "wins": data.wins,
                                         "losses": data.losses})
        node.flow_style = True
        return node
    
    @staticmethod
    def from_yaml(loader: yaml.SafeLoader, node):
        node = loader.construct_mapping(node)
        return Record(node["weight"], node["wins"], node["losses"])
yaml.SafeDumper.add_representer(Record, Record.to_yaml)
yaml.SafeLoader.add_constructor(Record.yaml_tag, Record.from_yaml)

WEIGHTS_MULTIPLIER = 0.1    # Multiplier subtracted depending on number of wins
RECORD_FILE = "./bot/resources/record.yaml"
member_records = {}
member_records: Dict[int, Record]
wheel_choices = {}
wheel_choices: Dict[mybot.discord.Member, str]

wheel = mybot.bot.create_group("wheel", description="Commands for spinning the wheel.",
                               guild_ids=[mybot.GUILD_ID])
# TODO: change to subgroup after fixed in py-cord
# wins = wheel.create_subgroup("wins", description="Commands for probability weights.",
#                              guild_ids=[mybot.GUILD_ID])
record = mybot.bot.create_group("record", description="Commands for win/loss/weight records.",
                             guild_ids=[mybot.GUILD_ID])

if os.path.exists(RECORD_FILE):
    try:
        with open(RECORD_FILE, "r") as myYaml:
            member_records = yaml.safe_load(myYaml)
    except Exception as e:
        print(f"Unable to import file {RECORD_FILE}.")


def export_wins():
    try:
        with open(RECORD_FILE, "w") as outfile:
            yaml.safe_dump(member_records, outfile, sort_keys=False)
    except Exception as e:
        print(f"Unable to export to {RECORD_FILE}. Exception caught: {e}")
        if os.path.exists(RECORD_FILE):
            os.remove(RECORD_FILE)


@wheel.command(
    name="add",
    description="Adds a member and choice combination to the wheel options.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="choice",
    description="The choice to add to the wheel.",
    required=True
)
@mybot.option(
    name="member",
    description="The member associated with the choice. Defaults to the message author.",
    required=False
)
async def add(ctx: mybot.discord.ApplicationContext, 
              choice: str, member: mybot.discord.Member = None):
    """
    Adds a member and their associated choice to the wheel options.

    Usage:
        /wheel add <choice> <@member>
    """
    if member is None:
        member = ctx.author
    if member in wheel_choices.keys():
        msg = f"Changed {member.mention} choice from \"{wheel_choices[member]}\" to \"{choice}\"."
    else: 
        msg = f"Added \"{choice}\" from {member.mention} to the wheel."
    wheel_choices[member] = choice
    await ctx.respond(msg)
    

@wheel.command(
    name="clear",
    description="Clears all choices in wheel or specific member's choice if specified.",
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
    embed = mybot.discord.Embed(
        title = "✨**Current Wheel Spinner**✨",
        color = mybot.discord.Color.dark_gold()
    )
    if wheel_choices is None or len(wheel_choices) == 0:
        embed.description = "*The wheel is empty!*"
        await ctx.respond(embed=embed, ephemeral=True)
        return
    description = ""
    for member, choice in wheel_choices.items():
        description += f"- {member.mention}: {choice}\n"
    embed.description = description
    await ctx.respond(embed=embed, ephemeral=True)


@wheel.command(
    name="spin",
    description="Spins a weighted wheel, with the options from specified members.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="clear",
    description="Clear wheel choices after spinning. Defaults to true.",
    required=False,
)
async def spin(ctx: mybot.discord.ApplicationContext, clear: bool = True):
    """
    Chooses a weighted random choice from current wheel options and prints the
    winner. A member's chances of winning the next spin decrease on a win, and
    increase on a loss. If clear set to False, the wheel options will be 
    retained.

    Usage:
        /wheel spin <clear>
    """
    num_members = len(wheel_choices)
    if num_members == 0:
        await ctx.respond("Cannot spin wheel with no choices.", ephemeral=True)
        return
    
    # Sets default weight as even (e.g. for 2 people, 50/50 chance)
    adjusted_weights = [100 / num_members] * num_members

    # Decreases odds for past wins, increases odds for past losses
    idx = 0
    for member in wheel_choices.keys():
        if member.id in member_records.keys():
            adjusted_weights[idx] *= 1 - (member_records[member.id].weight * WEIGHTS_MULTIPLIER)
        idx += 1
    # print(adjusted_weights)
    winner = choices(list(wheel_choices.keys()), weights=adjusted_weights)[0]
    winner_choice = wheel_choices[winner]

    # Update member record
    for member in wheel_choices.keys():
        if member.id not in member_records.keys():
            member_records[member.id] = Record()
        if member.id is winner.id:
            member_records[member.id].wins += 1
            if member_records[member.id].weight < 0:                
                member_records[member.id].weight = 0
            else:
                member_records[member.id].weight += 1
        else:
            member_records[member.id].losses += 1
            member_records[member.id].weight -= 1
    export_wins()
    
    if clear:
        wheel_choices.clear()
    await ctx.respond(f"The winner is {winner.mention} with \"{winner_choice}\"! Congratulations!")


@record.command(
    name="reset",
    description="Resets the record and weight for all members. Must be administrator.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.discord.default_permissions(administrator=True)
async def reset(ctx: mybot.discord.ApplicationContext):
    """
    Usage:
        /record reset
    """
    for member in member_records.keys():
        member_records[member] = Record()
    export_wins()
    await ctx.respond(f"Records reset.", ephemeral=True)


@record.command(
    name="view",
    description="Shows the current record for all past wheel spin members.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="show_weights",
    description="Show weights for each member. Defaults to False.",
    required=False,
)
async def wins_view(ctx: mybot.discord.ApplicationContext, show_weights: bool = False):
    """
    Requires server members intent.

    Usage:
        /record view <show_weights>
    """
    embed = mybot.discord.Embed(
        title = "✨**Wheel Spinner Wins**✨",
        color = mybot.discord.Color.dark_gold()
    )
    if member_records is None or len(member_records) == 0:
        embed.description = "*No previous winners!*"
        await ctx.respond(embed=embed, ephemeral=True)
        return
    description = ""
    sorted_member_records = dict(sorted(member_records.items(), key=lambda item: item[1].wins, reverse=True))
    for member_id, record in sorted_member_records.items():
        member = ctx.guild.get_member(int(member_id))
        description += f"- {member.mention} W: {record.wins}, L: {record.losses}\n"
        if show_weights:
            description += f" - Wt: {record.weight}\n"
            embed.set_footer(text="Higher weight decreases chances of winning.")
    embed.description = description
    await ctx.respond(embed=embed, ephemeral=True)