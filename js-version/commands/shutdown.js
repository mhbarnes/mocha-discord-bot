/*------------------------------------------------------------------------------
- Command: shutdown 
- Usage: !shutdown
- Description: Sends a signal to close the process running the bot. Can only
-   be executed by someone with admin permissions.
------------------------------------------------------------------------------*/
module.exports = {
    name: 'shutdown',
    description: 'Closes the bot.',
    execute(msg, args) {
        msg.channel.send('Shutting down...');
        client.destory();
    },
  };