### `Simple Twitch Bot `
___

#### `How to Use`

 * Pre-requirements
    * Twitch OAuth Token (You can get it in this address: https://twitchapps.com/tmi/ & more detail https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/)
    * You must use `python3 db.py` for create a database.
    * `sqlalchemy` module.
 * Run Bot
    * If you run it in command line this bot need 1 argument and 3 parameters. (Auth_Token:string, Bot_Username: string, #Channel_Name:string)
        * Example:
    `python3 index.py -r 'oauth:kerkjhrmmrir4mrjrmrvjtYrkkuemgrgkjrh' 'niceBotName' '#niceChannelName` 
 * Add Command  
    * You must run program with `-c` arguments and 2 parameter (command, command response) for add new command.
        * Example: `python3 -c 'newCommand' 'newCommandResponse'`
    * You must restart Twitch Bot after add new command.
  