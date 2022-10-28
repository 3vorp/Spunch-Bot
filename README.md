## **spunch bot** 

an atrocity made in discord.py by `Evorp#5819` because I was bored idk

use at your own risk lol

## installation and forking and all that stuff

requirements

- have python installed (who would have guessed)
- check the first line of the `main.py` file for specific libraries and modules to install via pip

go make a discord app at https://discord.com/developers

further instructions are at https://discordpy.readthedocs.io/en/stable/discord.html

create a `.env` file in the root folder with the following formatting:

```
TOKEN="your_bot_token_here"
```

this just makes the connection between the app and this repo

> **Warning**
> 
> **don't put your bot token in the main file, like seriously just don't**
> 
> also go to `main.py` and change the `BOT_ID` to your bot's id otherwise it will start getting into infinite loops and crash/break
> 
> make sure to change the hardcoded channel IDs (`SUGGEST_CHANNEL`, `LOGGING_CHANNEL`, `STARTUP_CHANNEL`, etc) to your desired ones

from there just run the python file and enjoy
