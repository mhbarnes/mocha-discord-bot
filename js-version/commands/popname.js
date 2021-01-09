/*------------------------------------------------------------------------------
- Command: popname
- Usage: !popname @<member>
- Description: Generates a random Poptropica name for a mentioned member.
-   If the user already has a role, then a denial message will be sent instead.
-   This can be overrided if the user has admin permissions.
------------------------------------------------------------------------------*/
const data = require('../PoptropicaNames.json')

var firstNames = new Array();
var lastNames = new Array();
const jsonPath = '../PoptropicaNames.json'

function loadNames() {
    $.getJSON(jsonPath, function (data) {
        firstNames = data.names.first;
        lastNames = data.names.last;
    })
    .error(function(){
        console.log('Error. Unable to load JSON');
    })
    .done(function() {
        console.log('JSON loaded successfully.')
    });
}

module.exports = {
    name: 'popname',
    description: 'Poptropica name generator. Use with !popname @<member>',
    execute(msg, args) {
      msg.reply('pong');
      msg.channel.send('pong');
    },
};