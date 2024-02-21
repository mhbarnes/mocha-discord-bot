# Introduction

The Mocha Discord Bot is a Python3 extensible command suite developed using the [py-cord Discord API](https://github.com/Pycord-Development/pycord). 

# Tutorial

## 1. Create a Discord Application

Go to the [Discord Developer Portal](http://discordapp.com/developers/applications) and create an Application, which allows you to utilize Discord's API. RealPython has an excellent tutorial on the process [here](https://realpython.com/how-to-make-a-discord-bot-python/). Make sure to take note of your **Bot's token**, as it will be needed later.

The minimum permissions needed for all commands to work are:

- Manage Roles
- Manage Nicknames
- Read Messages/View Channels
- Send Messages
- Send Messages in Threads
- Embed Links

Note that if you wish to use the `/wins view` command, then server members intent must be enabled.

![Image of server member intents setting.](docs/server-member-intents.png)

Once your bot is added to your server, you are ready to move on.

## 2. Download and Setup

Download/Clone the repository and install the required dependencies with `$ pip install -r requirements.txt`.

Next, run the setup script with `python setup.py`. This will copy the template .env and config.yaml files. 

Fill out the .env file with the following information. Make sure there are no spaces between the equal signs and your input.

- Your bot's token
  - Obtained from the [Discord Developer Portal](http://discordapp.com/developers/applications).
- Your server/guild ID
  - Go to User Settings > Advanced > Enable Developer Mode. Right click the name of your server at  the top or your server's icon on the left and select "Copy Server ID".
- The general member role ID
  - Only required for `/popname` command.

In the config.yaml file, adjust which commands to enable in your server. By default, only the `/cointoss` and `/shutdown` commands are enabled. To enable a command, replace the text next to the command names with "On", and disable with "Off".

## 3. Run the bot

When you are ready for your bot to go online, run the startup script with `python mochabot.py`.

# Commands

## cointoss command

Performs a coin flip.

Usage:

```
/cointoss <num_coins>
```

- *num_coins:* Optional. The number of coins to be flipped, up to 100. Defaults to 1.

## pasta command

Sends a copypasta from copypastas.json to the chat. If name is "list", the list of all available copypastas will be shown instead. If name is left empty, a random one will be sent.

By default, there is 1 copypasta available, though more can be added in copypastas.json

Usage: 

```bash
/pasta <name>
```

- *name*: Optional. The name of the copypasta to send. Defaults to empty (random copypasta).

## popname command

Generates a random, unique Poptropica name, renames a specified member in the server, and grants them the role specified by MEMBER_ROLE_ID. If they already have a Poptropica name, it will not be changed unless they have a higher role than MEMBER_ROLE_ID.

Usage: 

```bash
/popname <@member>
```

- *@member:* The member to give a Poptropica name and new role to.

## shutdown command

Shuts down the bot from within the server. Must be administrator, and is not visible in command list otherwise.

Usage: 

```bash
/shutdown
```

## wheel commands

### wheel add

Adds a member and their associated choice to the wheel's options.

Usage: 

```bash
/wheel add <@member> <choice>
```

- *@member:* The member associated with the choice.
- *choice:* The choice associated with the member.

### wheel clear

Removes a given member and their choice if user is specified. Otherwise, clears all options from the wheel.

Usage: 

```bash
/wheel clear <@member>
```

- *@member:* Optional. The member whose choice will be removed.

### wheel view

Shows the current members and choices on the wheel.

Usage: 

```bash
/wheel spin view
```

### wheel spin

Spins a weighted wheel, with the options provided from `/wheel add` and prints the winner. A member's chances of winning the next spin decrease on a win, and increase on a loss. If clear is set to false, the wheel options will be retained.

Usage: 

```bash
/wheel spin <clear>
```

- *clear:* Optional, defaults to True. Specifies whether the wheel's choices will be cleared.

## win commands

### wins reset

Resets the number of wins for all past wheel spins. Must be administrator.

Usage: 

```bash
/wins reset
```

### wins view

Shows the current number of wins for all past wheel spin members.

Usage: 

```bash
/wins view
```



# Planned Features

 - IMDB command
 - Wheel generation
