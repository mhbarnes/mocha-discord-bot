import BotInit as pb
import Commands.HelpCommand as hc
import random
import json


replies_file = 'Replies.json'   # JSON containing replies
replies = {}                    # Dictionary of reply strings


def cmd_reply():
    """
    Sends a random message to chat from replies JSON list.

    Usage:
        !reply
    """

    # Enable the help message
    hc.enabled_cmds['reply'] = True
    
    @pb.bot.command()
    async def reply(ctx, arg=None):
        await ctx.message.delete()

        # Generate random reply
        msg = random.choice(replies['replies'])
        await ctx.send(msg)
    return


def get_replies():
    """
    Loads list of replies from replies JSON.

    Returns:
        None.
    """

    with open(replies_file, 'r', encoding = 'utf-8') as myJson:
        replies.update(json.load(myJson))
    return