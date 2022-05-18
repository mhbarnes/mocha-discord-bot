import botinit as pb
import random
import json


names_file = '../shared/poptropica-names.json' # JSON containing possible poptropica names
poptropica_names = {}   # Dictionary of Poptropica names

# Loads list of Poptropica first/last names from Poptropica names JSON.
with open(names_file, 'r') as myJson:
    poptropica_names.update(json.load(myJson))


@pb.bot.slash_command(
    name="popname",
    description="Generates a random Poptropica name for @<member>.",
    guild_ids=[pb.MY_GUILD]
)
async def popname(ctx: pb.discord.ApplicationContext, member: pb.discord.Member):
    """
    Generates a random Poptropica name for @member. Command only
    works if @member does not have a role yet, EXCEPT if message author has a
    role higher than POPTROPICANS.

    Usage:
        /popname @member
    """
    author_toprole = ctx.author.top_role
    # await ctx.message.delete()
    
    # Retrieve guild variable for accessing server members
    guild = pb.bot.get_guild(pb.MY_GUILD)

    no_role = no_role_assigned(guild, member)
    override = author_toprole > guild.get_role(pb.POPTROPICANS)

    if no_role or override:
        new_nick = gen_popname()

        # Regenerates nickname until unused one is found
        while guild.get_member_named(new_nick) != None:
            new_nick = gen_popname()
        
        # Update nickname and role (if needed), and send message
        await member.edit(nick=new_nick)
        if no_role:
            await member.add_roles(guild.get_role(pb.POPTROPICANS))
        await ctx.respond(f'Henceforth {member.name} will be known as {member.mention}.')
    else:
        await ctx.respond(f'Fool. {member.mention} has already been assigned a sick role and rad name.')


def gen_popname():
    """
    Generates random Poptropica name of form 'first last'.

    Returns:
        String with random poptropica name.
    """
    return random.choice(poptropica_names['first']) + ' ' + random.choice(poptropica_names['last'])


def no_role_assigned(g, user):
    """
    Checks if the user being mentioned in the command doesn't have a role.

    Returns:
        True if user doesn't have a role, false otherwise.
    """
    if user.top_role == g.get_role(pb.EVERYONE):
        return True
    return False
