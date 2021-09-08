import BotInit as pb
import json

helpmsg_file = 'HelpMsg.json'   # JSON containing help messages
enabled_cmds = {}               # Dictionary to track enabled commands
help_msgs = {}                  # Dictionary of help messages


def cmd_help():
    """
    Lists all available enabled commands in chat.

    Usage:
        !help
    """
    
    # Enable the help message
    global enabled_cmds
    enabled_cmds['help'] = True

    @pb.bot.command()
    async def help(ctx):
        await ctx.message.delete()

        msg = '__**Available commands:**__\n\n'
        for cmd in enabled_cmds:
            if enabled_cmds[cmd] is True:
                msg = msg + help_msgs['helpmsgs'][cmd]['name'] + help_msgs['helpmsgs'][cmd]['msg'] + help_msgs['helpmsgs'][cmd]['usage'] + '\n'
        await ctx.send(msg)
    return


def get_helpmsgs():
    """
    Grabs list of help messages from help message JSON.

    Returns:
        None.
    """
    with open(helpmsg_file, 'r', encoding = 'utf-8') as myJson:
        help_msgs.update(json.load(myJson))