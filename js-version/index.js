/*******************************************************************************
 * File: index.js
 * Author: Michael Barnes
 * Last Modified: 12/22/2020
 * Description: Javascript Discord bot. Include commands that you will use.
*******************************************************************************/

/***************************************
 * Modules/Imports
***************************************/
// For importing loading token and channel ID
require('dotenv').config();
const TOKEN = process.env.TOKEN;

// For Discord api
const Discord = require('discord.js');
const bot = new Discord.Client();
bot.commands = new Discord.Collection();
const botCommands = require('./commands');

/***************************************
 * Global Variables
***************************************/
const prefix = "!";


// Import the commands specified in dir 'commands'
Object.keys(botCommands).map(key => {
    bot.commands.set(botCommands[key].name, botCommands[key]);
});

bot.login(TOKEN);

// Notify console that bot is online
bot.on('ready', () => {
  console.info(`Logged in as ${bot.user.tag}!`);
});

bot.on('message', msg => {
  // Check if message has the command prefix
  if (!msg.content.startsWith(prefix)) {
    return;
  }
  else {
    // Removes the prefix from the string
    msg.content = msg.content.substring(1);
  }
  // Parse the command by making command lowercase
  const args = msg.content.split(/ +/);
  const command = args.shift().toLowerCase();
  // Notify console that command is attempting to be called
  console.info(`Called command: ${command}`);

  if (!bot.commands.has(command)) {
    return;
  }

  try {
    bot.commands.get(command).execute(msg, args);
  } 
  catch (error) {
    console.error(error);
    msg.reply('there was an error trying to execute that command!');
  }
});
