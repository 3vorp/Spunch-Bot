# **spunch bot** 

## an atrocity made in discord.py by `Evorp#5819` because I was bored idk

the version of the bot I develop is not public mostly because it's a huge hazard — there's a ton of security vulnerablities I can't be bothered to fix

as a result it's mostly intended to be forked and run on your own, which is why it's on github in the first place

anyways bearing that in mind use this at your own risk lol

## installation and forking and all that stuff

requirements

- have python installed (who would have guessed)
- the following libraries:
    - discord.py (obviously)
    - random (used for 8ball command and a few other things)
    - wikipedia (used for wikipedia command)
    - json (used for the database)
    - datetime (used for startup message)
    - dotenv (used for bot token)

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
