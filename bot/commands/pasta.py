import bot.botinit as mybot
import random
from json import load


PASTA_FILE = "./bot/resources/copypastas.json"  # JSON containing copypastas
pastas = {}     # Dictionary of copypastas

with open(PASTA_FILE, "r", encoding = "utf-8") as myJson:
    pastas = load(myJson)

possible_pastas = list(pastas)

# Add "list" to available copypastas
pasta_list = "**__Available Copypastas:__**\n"
for pasta in sorted(pastas.keys()):
    pasta_list += f"{pasta}\n"
pastas["list"] = pasta_list


# Returns list of copypasta options for autocompletion.
def get_pastas(ctx: mybot.discord.AutocompleteContext):
    return [key for key in pastas.keys() if key.startswith(ctx.value.lower())]


@mybot.bot.slash_command(
    name="pasta",
    description="Sends a copypasta to chat from a list.",
    guild_ids=[mybot.GUILD_ID]
)
@mybot.option(
    name="name", 
    description="Specifies which copypasta to send. Leave empty for random.",
    required=False,
    autocomplete=get_pastas
)
async def pasta(ctx: mybot.discord.ApplicationContext, name: str):
    """
    Outputs a copypasta. If option is not specified, a random copypasta is used.

    Usage:
        /pasta <option>
    """
    is_list = name == "list"
    if name is None or name == "":
        # If option blank, send random copypasta
        random_key = random.choice(possible_pastas)
        msg = f"**{random_key}**\n{pastas[random_key]}"
    elif is_list:
         msg = pastas[name]
    else:
         msg = f"**{name}**\n{pastas[name]}"
    await ctx.respond(msg, ephemeral=is_list)
