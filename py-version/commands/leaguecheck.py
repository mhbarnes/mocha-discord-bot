import botinit as pb


# def cmd_leaguecheck():
#     """
    
#     Usage:
#         !leaguecheck on
#         !leaguecheck off
#     """
#     # Enable the help message
#     global enabled_cmds
#     enabled_cmds['leaguecheck'] = True

#     #TODO add argument handling
#     @pb.bot.command()
#     @pb.commands.has_permissions(administrator=True)
#     async def leaguecheck(ctx):
#         # Retrieve guild ID for accessing server members
#         guild = pb.bot.get_guild(pb.MY_GUILD)
#         await ctx.send(f'League check :leg:')
#         # TODO iteerate through member list, check if any playing league & in voice chat
#     return
