import BotInit as pb
import Commands.HelpCommand as hc
import random
import json


pasta_file = 'Copypastas.json'  # JSON containing copypastas
pastas = {}


def cmd_pasta():
    """
    Outputs a copypasta. If option is not specified, a random copypasta is used.

    Usage:
        !pasta <option>
    """

    # Enable the help message
    hc.enabled_cmds['pasta'] = True

    @pb.bot.command()
    async def pasta(ctx, arg=None):
        await ctx.message.delete()

        option = arg

        if option is None:
            # If option blank, send random copypasta
            random_key = random.choice(list(pastas['copypastas']))
            msg = pastas['copypastas'][random_key]
            await ctx.send(msg)
            return
        else:
            # Convert the copypasta option to lowercase
            option = arg.lower()

        # Process option
        if option == "list":
            # List all available copypastas
            msg = ".\n"

            for pasta in sorted(pastas['copypastas'].keys()):
                msg += '[' + pasta + ']\n'
        elif option in pastas['copypastas'].keys():
            msg = pastas['copypastas'][option]
        else:
            return
        
        await ctx.send(msg)
    return


def get_pastas():
    """
    Loads list of copypastas from copypastas JSON.

    Returns:
        None.
    """

    with open(pasta_file, 'r', encoding = 'utf-8') as myJson:
        pastas.update(json.load(myJson))
    return