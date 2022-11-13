# I know this should probably be a json file but this is way easier to deal with so cope harder lol

all = '''
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
— `{PREFIX}rps`: rock paper scissors against spunch bot
— `{PREFIX}nut`: sacrifice NUT to me

**specific info for a command can be found by running**
```{PREFIX}help <command>```
''' # can't use an f string since PREFIX can't really be imported easily, instead it's evaluated in main file

#using 2d lists to separate each command out so that I can iterate through it in a for loop in the main program really really easily

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
**NOTES:**

if no/multiple wikipedia articles are found it will raise an error, you have to be really specific for some reason idk blame the library i used
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
**NOTES:**

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
{PREFIX}setprefix .
{PREFIX}prefix reset
```

**NOTES:**

prefix can only be one character long due to how i wrote basically the entire bot
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
{PREFIX}info <command>
{PREFIX}help
{PREFIX}info
```
**EXAMPLE:**
```
{PREFIX}help wikipedia
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
**NOTES:**

questions have to be yes/no formatted for the bot to make sense
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
**NOTES:**

if you don't specify what you're playing spunch bot will decide for you randomly
'''

], [('nut'),

'''
sacrifice NUT to me, adds one to global counter

**SYNTAX:**
```
{PREFIX}nut
```
'''
]
]
