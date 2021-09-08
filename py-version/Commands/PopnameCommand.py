import BotInit as pb
import Commands.HelpCommand as hc
import random
import json


names_file = 'PoptropicaNames.json' # JSON containing possible poptropica names
poptropica_names = {}               # Dictionary of Poptropica names


def cmd_popname():
    """
    Generates a random Poptropica name for @member. Command only
    works if @member does not have a role yet, EXCEPT if message author has a
    role higher than POPTROPICANS.

    Usage:
        !popname @<member>
    """

    # Enable the help message
    hc.enabled_cmds['popname'] = True

    @pb.bot.command()
    async def popname(ctx, member: pb.discord.Member):
        author_toprole = ctx.message.author.top_role
        await ctx.message.delete()
        
        # Retrieve guild ID for accessing server members
        guild = pb.bot.get_guild(pb.MY_GUILD)

        if check_role_assigned(guild, member) == True:
            new_nick = gen_popname()

            # Checks if nickname is already in place
            while guild.get_member_named(new_nick) != None:
                new_nick = gen_popname()

            # Update nickname and role
            await member.edit(nick=new_nick)
            await member.add_roles(guild.get_role(pb.POPTROPICANS))
            await ctx.send(f'Henceforth {member.name} will be known as {member.mention}.')
        elif author_toprole > guild.get_role(pb.POPTROPICANS):
            # If member has higher than base permissions, allow for override
            new_nick = gen_popname()

            # Checks if nickname is already in place
            while guild.get_member_named(new_nick) != None:
                new_nick = gen_popname()

            # Update nickname and role
            await member.edit(nick=new_nick)
            await ctx.send(f'Henceforth {member.name} will be known as {member.mention}.')
        else:
            await ctx.send(f'Fool. {member.mention} has already been assigned a sick role and rad name.')
    return


def get_popnames():
    """
    Loads list of Poptropica first/last names from Poptropica names JSON.

    Returns:
        None.
    """
    with open(names_file, 'r') as myJson:
        poptropica_names.update(json.load(myJson))
    return


def gen_popname():
    """
    Generates random Poptropica name of form 'first last'.

    Returns:
        String with random poptropica name.
    """
    return random.choice(poptropica_names['names']['first']) + ' ' + random.choice(poptropica_names['names']['last'])


def check_role_assigned(g, user):
    """
    Checks if the user being mentioned in the command doesn't have a role.

    Returns:
        True if user doesn't have a role, false otherwise.
    """
    if user.top_role == g.get_role(pb.EVERYONE):
        return True
    return False
