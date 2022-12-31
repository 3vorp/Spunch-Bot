# I know this should probably be a json file but this is way easier to deal with so cope harder lol

help_all = '''
an atrocity made in discord.py by `{DEVELOPER}` because I was bored idk

__**COMMANDS AVAILABLE:**__ *(more to be added soon™)*

**utility:**

— `{PREFIX}wikipedia`: returns wikipedia article
— `{PREFIX}feedback`, `{PREFIX}suggest`: suggest stuff to implement
— `{PREFIX}prefix`, `{PREFIX}setprefix`: change prefix for server, add `reset` to reset prefix
— `{PREFIX}length`, `{PREFIX}len`: returns word and character count of string
— `{PREFIX}github`: show github listing
— `{PREFIX}help`, `{PREFIX}info`: if no command mentioned shows main help message, otherwise shows specific help for that command

**fun:**

— `{PREFIX}say`: say stuff with bot
— `{PREFIX}embed`: like `{PREFIX}say` but better (use `{PREFIX}help embed` for the specific syntax required)
— `{PREFIX}8ball`, `{PREFIX}ball`: random answers for random questions
— `{PREFIX}dice`, `{PREFIX}roll`: roll any number of dice with any number of sides
— `{PREFIX}mock`: MoCk a sTrInG Of tExT To lOoK LiKe tHiS
— `{PREFIX}rps`: rock paper scissors against spunch bot
— `{PREFIX}nut`: sacrifice NUT to me, adds one to global counter

**specific info for a command can be found by running**
```{PREFIX}help <command>```
''' # can't use an f string since PREFIX can't really be imported easily, instead it's evaluated in main file



help_footer = '''
go suggest stuff using {PREFIX}feedback if you want me to add stuff ig
'''



help_not_found = '''
no command with that name was found, use `{PREFIX}help` for the full list
'''



#using 2D lists to separate each command out so that I can iterate through it in a for loop in the main program really really easily



help_list = [ # I know this is hard to read but it's a lot better than having it all in one file so oh well

[('wikipedia',), # even when there's no aliases it has to be in a tuple to be correctly parsed

'''
returns wikipedia article

**SYNTAX:**
```
{PREFIX}wikipedia <wikipedia article>
```
**EXAMPLE:**
```
{PREFIX}wikipedia discordapp
```
**NOTE:**

if multiple possible articles are found it will just pick a random one
'''

], [('feedback','suggest'), # the first entry in the tuple is always the one displayed in the title

'''
suggest stuff to implement

**SYNTAX:**
```
{PREFIX}feedback <suggestion(s)>
{PREFIX}suggest <suggestion(s)>
```
**EXAMPLE:**
```
{PREFIX}feedback add actually decent errors
```
**NOTE:**

there is currently no way to see if feedback has been accepted, but this is planned for the future
'''

], [('prefix','setprefix'),

'''
set prefix for current server

add reset to reset the prefix (obviously)

**SYNTAX:**
```
{PREFIX}prefix <prefix>
{PREFIX}setprefix <prefix>
{PREFIX}prefix reset
{PREFIX}setprefix reset
```
**EXAMPLES:**
```
{PREFIX}setprefix !
{PREFIX}prefix reset
```

**NOTE:**

currently you can only have one prefix per server, so no command aliases for now
'''

], [('length','len'),

'''
return word and character count of string

**SYNTAX:**
```
{PREFIX}length <message>
{PREFIX}len <message>
```
**EXAMPLE:**
```
{PREFIX}length this is a string of text
```
'''

], [('github',),

'''
show github listing

**SYNTAX:**
```
{PREFIX}github
```
'''

], [('help','info'),

'''
if no command mentioned, shows main help message

otherwise, shows specific help for that command

**SYNTAX:**
```
{PREFIX}help <command>
{PREFIX}info <all>
{PREFIX}help
```
**EXAMPLE:**
```
{PREFIX}info wikipedia
{PREFIX}help all
```
'''

], # fun section

[('say',),

'''
make the bot say stuff

**SYNTAX:**
```
{PREFIX}say <message>
```
**EXAMPLE:**
```
{PREFIX}say sentience acquired
```
'''

], [('embed',),

'''
like `{PREFIX}say`, but better

generates a custom embed

**SYNTAX:**
```
{PREFIX}embed <title>, <description>, <color>, <footer>
```
**EXAMPLE:**
```
{PREFIX}embed this is an example embed, epic description that **supports markdown**, #7289DA, epic small text
```
**NOTES:**

to omit a portion (e.g. if you don't want to add a description), just replace that entry in the list with a space

**keep the commas for ordering purposes, just leave the area between them blank**
```
{PREFIX}embed title, ,#00ff00, no description will be loaded
```
you can do this multiple times in a row as well:
```
{PREFIX}embed now it will just use the default yellow color,,, footer
```
you can also omit stuff at the end completely if you don't want a footer and/or color
```
{PREFIX}embed example title, no footer necessary
```
'''

], [('8ball','ball'),

'''
random answers for random questions

**SYNTAX:**
```
{PREFIX}8ball <question>
{PREFIX}ball <question>
```
**EXAMPLE:**
```
{PREFIX}8ball is anything real
```
**NOTE:**

questions have to be yes/no formatted for the bot to make sense
'''

], [('dice','roll'),

'''
roll any number of dice with any number of sides

**SYNTAX:**
```
{PREFIX}dice <number of dice> <number of sides>
{PREFIX}roll
```

**EXAMPLE:**
```
{PREFIX}dice 3 12
{PREFIX}roll 4
{PREFIX}dice
```

**NOTES:**

default is one 6 sided dice
you can provide how many dice without providing how many sides, bot will assume 6 by default
'''

], [('mock',),

'''
MoCk a sTrInG Of tExT To lOoK LiKe tHiS

**SYNTAX:**
```
{PREFIX}mock <message>
```

**EXAMPLE:**
```
{PREFIX}mock My name is Walter Hartwell White. I live at 308 Negra Arroyo Lane, Albuquerque, New Mexico 87104.
```
'''

], [('rps',),

'''
rock paper scissors against spunch bot

**SYNTAX:**
```
{PREFIX}rps <choice>
{PREFIX}rps
```
**EXAMPLES:**
```
{PREFIX}rps
{PREFIX}rps rock
{PREFIX}rps paper
{PREFIX}rps scissors
```
**NOTE:**

if you don't specify what you're playing spunch bot will decide for you randomly
'''

], [('nut',),

'''
sacrifice NUT to me, adds one to global counter

**SYNTAX:**
```
{PREFIX}nut
{PREFIX}nut amount
{PREFIX}nut total
```
**NOTE:**

just for fun, don't take this command too seriously lol
'''
]
]



# decided to put error messages here as well since they technically help you lol



error_generic = '''
too lazy to implement proper errors but you probably:

— sent too much stuff
— didn't send enough stuff
— sent something that wasn't a command

**use `{PREFIX}help` for a list of commands**
'''



error_database = '''\033[91m\033[1m
IMPORTANT WARNING: Check the README.md more closely:

There are two possible reasons for this error appearing:

1. You didn't add a database. Copy the `database_example.json` file and rename it to `database.json`.

2. You are using the Code Runner Visual Studio Code extension. Check the bottom of README.md for a code snippet to paste that will fix this issue.

The bot will mostly work without a database, however commands such as `prefix` and `nut` will result in a LOT of errors.
'''