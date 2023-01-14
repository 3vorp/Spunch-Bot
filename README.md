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
    - os (used for database/token stuff)
    - random (used for 8ball command and a few other things)
    - wikipedia (used for wikipedia command)
    - json (used for the database)
    - time (used for startup message)
    - dotenv (used for bot token)

go make a discord app at https://discord.com/developers

further instructions are at https://discordpy.readthedocs.io/en/stable/discord.html

copy the `.env.example` file and rename it to `.env`

insert your bot token into where it says `"your_bot_token_here"`, surrounded with double quotes

this just makes the connection between the actual bot and these python files

> **Warning**
>
> **your bot token is basically your bot password, be careful with it and do not post it anywhere**

## using a database properly

in your main working folder (the one that this file and the `RUN_ME.py` file are contained in) create a file called `database.json`.

it just uses regular json formatting, read the example file for specifics

## config

`config.py` contains most of the hardcoded stuff like colors and channel ids, so feel free to edit that to change most defaults

oh also if you're renaming the bot etc the frame of spongeboy used on static images is always 106

# IF YOU ARE USING VISUAL STUDIO CODE (VSCODE) AND ARE USING THE CODE RUNNER EXTENSION:

the default method that the Code Runner extension uses for running a python file is by running it straight from the path

however since there are multiple files in the directory this can and will cause issues

to resolve this go into the `settings.json` file (contained in your appdata/application support folder under `Code/User/settings.json`) and paste in the following code
```json
"code-runner.executorMap": {
    "python": "cd $dir && python3 $fileName",
}
```

this will ensure that you are changing to the proper directory _before_ running the file, allowing you to access all the other files contained in the directory (database, config, etc)

from there just run the python file and enjoy
