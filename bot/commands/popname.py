import bot.botinit as mybot
import random
import json


NAMES_FILE = "./bot/resources/poptropica-names.json" # JSON containing possible poptropica names
poptropica_names = {}   # Dictionary of Poptropica names

# Loads list of Poptropica first/last names from Poptropica names JSON.
with open(NAMES_FILE, "r", encoding = "utf-8") as myJson:
    poptropica_names.update(json.load(myJson))

# Generates random Poptropica name of form "first last".
def gen_popname():
    return f"{random.choice(poptropica_names['first'])} {random.choice(poptropica_names['last'])}"

# Checks if the user being mentioned in the command has a role.
def has_role_assigned(g: mybot.discord.Guild, user: mybot.discord.Member):
    if user.top_role == g.get_role(mybot.EVERYONE):
        return False
    return True


@mybot.bot.slash_command(
    name="popname",
    description="Generates a random Poptropica name for @<member>.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="member", 
    description="The member to give a Poptropica name to.",
    required=True
)
async def popname(ctx: mybot.discord.ApplicationContext, member: mybot.discord.Member):
    """
    Generates a random Poptropica name for @member. Command only
    works if @member does not have a role yet, EXCEPT if message author has a
    role higher than POPTROPICANS.

    Usage:
        /popname <@member>
    """
    author_toprole = ctx.author.top_role
    
    # Retrieve guild variable for accessing server members
    guild = mybot.bot.get_guild(mybot.GUILD_ID)

    has_role = has_role_assigned(guild, member)
    no_override = author_toprole < guild.get_role(mybot.MEMBER_ROLE_ID)

    if has_role or no_override:
        await ctx.respond(f"Fool. {member.mention} has already been assigned a sick role and rad name.")
        return
    new_nick = gen_popname()

    # Regenerates nickname until unused one is found
    while guild.get_member_named(new_nick) != None:
        new_nick = gen_popname()
    
    # Update nickname and role (if needed), and send message
    try:
        await member.edit(nick=new_nick)
    except:
        msg = f"Unable to change nickname of {member.name}."
        print(msg)
        await ctx.respond(msg, ephemeral=True)
    try:
        await member.add_roles(guild.get_role(mybot.MEMBER_ROLE_ID))
    except:
        msg = f"Unable to change roles of {member.name}."
        print(msg)
        await ctx.respond(msg, ephemeral=True)
    await ctx.respond(f"Henceforth {member.name} will be known as {member.mention}.")
