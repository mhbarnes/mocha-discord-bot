module.exports = {
    name: 'ping',
    description: 'Basic test command. Replies with \"pong\".',
    execute(msg, args) {
      msg.reply('pong');
      msg.channel.send('pong');
    },
  };