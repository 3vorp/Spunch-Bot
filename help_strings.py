import config
# I know this should probably be a json file but this is way easier to deal with so cope harder lol

all = '''
an atrocity made in discord.py by `{DEVELOPER}` because I was bored idk

**For specific commands, run `{PREFIX}help <command>`

__**COMMANDS AVAILABLE:**__ *(more to be added soon™)*

**utility:**

— `{PREFIX}wikipedia`: returns wikipedia article
— `{PREFIX}feedback`, `{PREFIX}suggest`: suggest stuff to implement
— `{PREFIX}prefix`, `{PREFIX}setprefix`: change prefix for server, add `reset` to reset prefix
— `{PREFIX}length`, `{PREFIX}len`: returns word and character count of string
— `{PREFIX}github`: show github listing
— `{PREFIX}help`, `{PREFIX}info`: shows this message, should be pretty obvious lol

**fun:**

— `{PREFIX}say`: say stuff with bot
— `{PREFIX}embed`: like ~say but better (use `{PREFIX}help embed` for the specific syntax required)
— `{PREFIX}8ball`, `{PREFIX}ball`: random answers for random questions
— `{PREFIX}rps`: rock paper scissors against spunch bot
— `{PREFIX}crimes`: show all of my crimes
— `{PREFIX}nut`: sacrifice NUT to me''' # can't use an f string since PREFIX can't really be imported easily, instead it's evaluated in main file

# yes this should probably be a dictionary but it makes iterating through the loop a lot easier imo

help_list = [ # I know this is hard to read but it's a lot better than having it all in one file so oh well
# order of arguments: what should be in the command itself, title, description
    [
        'wikipedia',
        'help for {PREFIX}wikipedia',
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
    ],
    [
        ('feedback','suggest'),
        'help for {PREFIX}feedback',
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
    ],
    [
        ('prefix','setprefix'),
        'help for {PREFIX}prefix',
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
    ],
    [
        ('length','len'),
        'help for {PREFIX}length',
        '''
return word and character count of string

**SYNTAX:**
{PREFIX}length <message>
{PREFIX}len <message>

**EXAMPLE:**
{PREFIX}len this is a string of text
        '''
    ]
]
