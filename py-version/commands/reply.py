import botinit as pb
import random
import json


replies_file = '../shared/Replies.json'   # JSON containing replies
replies = {}    # Dictionary of reply strings

# Loads list of replies from replies JSON.
with open(replies_file, 'r', encoding = 'utf-8') as myJson:
    replies.update(json.load(myJson))

@pb.bot.slash_command(
    name="reply",
    description="Sends a random message to chat from a list.",
    guild_ids=[pb.MY_GUILD]
)
async def reply(ctx: pb.discord.ApplicationContext):
    """
    Sends a random message to chat from replies JSON list.

    Usage:
        /reply
    """
    # Generate random reply
    msg = random.choice(replies['replies'])
    await ctx.respond(msg)
