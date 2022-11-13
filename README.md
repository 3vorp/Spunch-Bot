## **spunch bot** 

an atrocity made in discord.py by `Evorp#5819` because I was bored idk

use at your own risk lol

## installation and forking and all that stuff

requirements

- have python installed (who would have guessed)
- check the first line of the `main.py` file for specific libraries and modules to install via pip

go make a discord app at https://discord.com/developers

further instructions are at https://discordpy.readthedocs.io/en/stable/discord.html

create a `.env` file in the root folder, following the formatting of the `.env.example` file:

this just makes the connection between the app and the python files

> **Warning**
> 
> **your bot token is basically your bot password, be careful with it and do not post it anywhere**
>  
> make sure to change the hardcoded channel IDs (`SUGGEST_CHANNEL`, `STARTUP_CHANNEL`, etc) to your desired ones in the `main.py` file.

## using a database properly

in your main working folder (the one that this file and the `main.py` file is contained in) create a file called `database.json`.

it just uses regular json formatting, read the example file for specifics

also you can edit `config.py` to change some defaults like prefixes and colors

from there just run the python file and enjoy
