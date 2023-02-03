'''
I tried making this a json but dealing with super long strings really didn't work well,
and honestly this is a lot easier to read,
plus in the main file you can just use info_strings.variable to access it
'''



# as PREFIX is evaluated per-command it's parsed in the main file instead using eval()
help_all = '''
an atrocity made in discord.py by `Evorp#5819` because I was bored idk

**COMMANDS AVAILABLE:**

**utility:**

— `{PREFIX}wikipedia`, `{PREFIX}wiki`, `{PREFIX}w`: returns wikipedia article
— `{PREFIX}feedback`, `{PREFIX}f`, `{PREFIX}suggest`: suggest stuff to implement
— `{PREFIX}setprefix`, `{PREFIX}prefix`, `{PREFIX}p`: change prefix for server, add `reset` to reset
— `{PREFIX}setannouncements`, `{PREFIX}sa`: change announcement channel for server, add `none` to disable
— `{PREFIX}changelog`, `{PREFIX}announcement`: show bot update changelogs
— `{PREFIX}length`, `{PREFIX}len`, `{PREFIX}l`: returns word and character count of string
— `{PREFIX}github`, `{PREFIX}git`, `{PREFIX}g`: show github listing
— `{PREFIX}help`, `{PREFIX}h`, `{PREFIX}info`, `{PREFIX}i`: if no command mentioned shows main help message, otherwise shows specific help for that command

**fun:**

— `{PREFIX}say`, `{PREFIX}s`: say stuff with bot
— `{PREFIX}embed`, `{PREFIX}e`: like `{PREFIX}say` but better (use `{PREFIX}help embed` for the specific syntax required)
— `{PREFIX}ball`, `{PREFIX}8ball`, `{PREFIX}b`: random answers for random questions
— `{PREFIX}dice`, `{PREFIX}d`, `{PREFIX}roll`, `{PREFIX}r`: roll any number of dice with any number of sides
— `{PREFIX}mock`, `{PREFIX}m`: MoCk a sTrInG Of tExT To lOoK LiKe tHiS
— `{PREFIX}uwu`, `{PREFIX}u`, `{PREFIX}owo`: uwu-ify text, i hate this as much as you do
— `{PREFIX}rockpaperscissors`, `{PREFIX}rps`: rock paper scissors against me
— `{PREFIX}nut`, `{PREFIX}n`: sacrifice NUT to me, adds one to global counter

**specific info for a command can be found by running**
```{PREFIX}help <command>```
'''



# dictionaries have a lot of limitations with storing data, similar to json
# there's no way to have aliases in the conventional sense, like how using the tuple here works
# so a 2d list with standardized indexing ends up working a lot better for stuff like the help command
# however a dictionary can be parsed from the list contents for stuff like slash command descriptions



help_list = (

(('wikipedia', 'wiki', 'w'),

'returns wikipedia article',

'''
**SYNTAX:**
```
{PREFIX}wikipedia <wikipedia article>
```
**EXAMPLE:**
```
{PREFIX}wikipedia discord
```
**NOTE:**

will show all possible options if you aren't specific enough
'''

), (('feedback', 'f', 'suggest'),

'suggest stuff to implement',

'''
**SYNTAX:**
```
{PREFIX}feedback <suggestion(s)>
```
**EXAMPLE:**
```
{PREFIX}feedback slash commands when
```
**NOTE:**

there is currently no way to see if feedback has been accepted, but this is planned for the future
'''

), (('setprefix', 'prefix', 'p'),

'set prefix for current server',

'''
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

currently you can only have one prefix per server, so no prefix aliases for now
'''

), (('setannouncements', 'sa'),

'change announcement channel for server',

'''
**SYNTAX:**
```
{PREFIX}setannouncements
{PREFIX}setannouncements reset
{PREFIX}sa none
```

**NOTES:**
by default the first available channel is set as the announcement one
the channel the command is sent in will become the new one when used
adding `none` will turn announcements for the server off
`reset` will bring it back to the first available one
'''

), (('changelog', 'announcement'),

'show bot update changelogs',

'''
**SYNTAX:**
```
{PREFIX}changelog <amount>
```

**EXAMPLE:**
```
{PREFIX}changelog 3
```

**NOTES:**

by default only provides one
orders by oldest to newest
causes a lot of spam, beware of using large numbers
'''

), (('length', 'len', 'l'),

'return word and character count of string',

'''
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

), (('github', 'git', 'g'),

'show github listing',

'''
**SYNTAX:**
```
{PREFIX}github
```
'''

), (('help', 'h', 'info', 'i'),

'if no command mentioned, shows main help message; otherwise, shows specific help for that command',

'''
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

), # fun section

(('say', 's'),

'make the bot say stuff',

'''
**SYNTAX:**
```
{PREFIX}say <message>
```
**EXAMPLE:**
```
{PREFIX}say sentience acquired
```
'''

), (('embed', 'e'),

'like `{PREFIX}say`, but better',

'''
**SYNTAX:**
```
{PREFIX}embed <title>; <description>; <hex color>; <footer>; <footer image>; <thumbnail image>
{PREFIX}embed <image>
```
**EXAMPLES:**
```
{PREFIX}embed this is an example embed; epic description that **supports markdown**; #7289DA; epic small text; https://3vorp.github.io/favicon.png; https://i.imgur.com/hAuUsnD.png

{PREFIX}embed https://media1.tenor.com/images/8dc53503f5a5bb23ef12b2c83a0e1d4d/tenor.gif
```
**NOTES:**

to omit a portion (e.g. if you don't want to add a description), just leave that entry in the list blank or a space

**keep the semicolons for ordering purposes, just leave the area between them blank**
```
{PREFIX}embed title;; #00ff00; no description will be loaded
```
you can do this multiple times in a row as well:
```
{PREFIX}embed now it will just use the default yellow color;;; footer
```
you can also omit stuff at the end completely if you don't want a footer/color/images/description
```
{PREFIX}embed example title; no footer/image necessary
```
if the first argument is a url (starts with https:// or http://), it will try and find an image with that url
it will give a nonloading image if the url doesn't point to an image, since that's how I made the bot
'''

), (('ball', '8ball', 'b'),

'random answers for random questions',

'''
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

), (('dice', 'd', 'roll', 'r'),

'roll any number of dice with any number of sides',

'''
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

), (('mock', 'm'),

'MoCk a sTrInG Of tExT To lOoK LiKe tHiS',

'''
**SYNTAX:**
```
{PREFIX}mock <message>
```

**EXAMPLE:**
```
{PREFIX}mock My name is Walter Hartwell White. I live at 308 Negra Arroyo Lane, Albuquerque, New Mexico 87104.
```
'''

), (('uwu', 'u', 'owo'),

'uwu-ify text, i hate this as much as you do',

'''
**SYNTAX:**
```
{PREFIX}uwu <message>
```

**EXAMPLE:**
```
{PREFIX}uwu i'm like a lion stalking its prey from the bushes, except i'm a grown man stalking children under the age of 9
```
'''

),
(('rockpaperscissors', 'rps'),

'rock paper scissors against me',

'''
**SYNTAX:**
```
{PREFIX}rockpaperscissors <choice>
{PREFIX}rps
```
**EXAMPLES:**
```
{PREFIX}rockpaperscissors
{PREFIX}rps rock
{PREFIX}rockpaperscissors paper
{PREFIX}rps scissors
```
**NOTE:**

if you don't specify what you're playing i will decide for you randomly
'''

), (('nut', 'n'),

'sacrifice NUT to me, adds one to global counter',

'''
**SYNTAX:**
```
{PREFIX}nut
{PREFIX}nut amount
{PREFIX}nut total
```
**NOTE:**

just for fun, don't take this command too seriously lol
'''
)
)


help_dict = {i[0][0]: i[1] for i in help_list}

# generic messages that didn't fit anywhere else
help_footer = '''
go suggest stuff using {PREFIX}feedback if you want me to add stuff ig
'''

help_not_found = '''
no command called "{search}" was found, use `{PREFIX}help` for the full list
'''



# ended up using a prefix system of sorts



error_database = '''\033[91m\033[1m
IMPORTANT WARNING: Check the README.md more closely:

There are two possible reasons for this error appearing:

1. You didn't add a database. Copy the `database_example.json` file and rename it to `database.json`.

2. You are using the Code Runner Visual Studio Code extension. Check the bottom of README.md for a code snippet to paste that will fix this issue.

The bot will mostly work without a database, however commands such as `prefix` and `nut` will result in a LOT of errors.
'''