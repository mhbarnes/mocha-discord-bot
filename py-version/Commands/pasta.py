import botinit as pb
import random
import json


pasta_file = '../shared/copypastas.json'  # JSON containing copypastas
pastas = {}     # Dictionary of copypastas


with open(pasta_file, 'r', encoding = 'utf-8') as myJson:
    pastas = json.load(myJson)
pastas["list"] = ""

def get_pastas(ctx: pb.discord.AutocompleteContext):
    """
    Returns list of copypasta options for autocompletion.

    Returns:
        List of strings.
    """
    return [key for key in pastas.keys() if key.startswith(ctx.value.lower())]

@pb.bot.slash_command(
    name="pasta",
    description="Sends a copypasta to chat from a list.",
    guild_ids=[pb.MY_GUILD]
)
@pb.option(
    name="name", 
    description="Specifies which copypasta to send. Leave empty for random.",
    required=False,
    autocomplete=get_pastas
)
async def pasta(ctx: pb.discord.ApplicationContext,
    name: str
):
    """
    Outputs a copypasta. If option is not specified, a random copypasta is used.

    Usage:
        /pasta <option>
    """
    if name is None or name == "":
        # If option blank, send random copypasta
        random_key = random.choice(list(pastas))
        msg = pastas[random_key]
    elif name == "list":
        # List all available copypastas
        msg = "**__Available Copypastas:__**\n"
        for pasta in sorted(pastas.keys()):
            if pasta != "list":
                msg += pasta + '\n'
    else:
        # Send the requested copypasta
        msg = pastas[name]
    await ctx.respond(msg)