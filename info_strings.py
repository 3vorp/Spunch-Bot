'''
while initially planned as a json, a lot of parsing ended up being required
so a second file ended up working far better for generating variables

I needed a way that would accommodate all formats I'd be parsing the text as
this resulted in the actual strings going into `help_categorized`
it's hard to parse and harder to read, sorted as
```
command category:
    command name:
        tuple of aliases,
        short description,
        syntax/example/notes
```

with two layers of nesting

it's also hard to iterate over or do anything meaningful with
so I generated `help_list` from the contents
it essentially fully removes the dictionary aspect making it a basic 2d list
```
command name:
    tuple of aliases
    short description,
    syntax/example/notes
```

this is still sorted via index rather than via key though
so if you want a specific description from a command etc there's no way
`help_dict` is generated because of this, for use in slash command descriptions etc
it's pretty easy to read through and parse:
```
main command name: short description
```

finally, the reason why command categories were necessary to have in `help_categorized`
`help_string` contains a formatted version of every command with description and categorized
meaning that the commands would need some form of category system to have stuff in the right place

prior to me using this system I'd have to write down everything twice
but now it's procedurally generated from the contents of `help_categorized`
'''



help_categorized = {
'utility': (
(

('wikipedia', 'wiki', 'w'),

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

),
(

('feedback', 'f', 'suggest'),

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

),
(

('length', 'len', 'l'),

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

),
(

('license', 'tos'),

'show license',

'''
**SYNTAX:**
```
{PREFIX}license
```
'''

),
(

('github', 'git', 'g'),

'show github listing',

'''
**SYNTAX:**
```
{PREFIX}github
```
'''

),
(

('help', 'h', 'info', 'i'),

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

)
), 'server': (
(

('setprefix', 'prefix', 'p'),

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

),
(

('setannouncements', 'sa'),

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

),
(

('changelog', 'announcement'),

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

),
(

('say', 's'),

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

),
(

('embed', 'e'),

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

)
), 'fun': (
(

('ball', '8ball', 'b'),

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

),
(

('dice', 'd', 'roll', 'r'),

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

),
(

('mock', 'm'),

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

),
(

('uwu', 'u', 'owo'),

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
(

('behave',),

'for when i\'m being naughty 😈',

'''
**SYNTAX:**
{PREFIX}behave

**NOTES:**
if you aren't authorized to MAKE me behave I may perform a bit of trolling
'''

),
(

('bean',),

'ban but  b e a n s',

'''
**SYNTAX:**
```
{PREFIX}bean <user> <reason>
```
**EXAMPLE:**
```
{PREFIX}bean @everyone plotting my demise
'''

),
(

('rockpaperscissors', 'rps'),

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

),
(

('nut', 'n'),

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
}


# gets rid of one "layer" of the list and flattens it down to a more usable version
help_list = [i for j in help_categorized.values() for i in j]



# uses the flattened help list and formats it into a much more convenient dictionary
help_dict = {i[0][0]: i[1].replace('{PREFIX}', '/') for i in help_list}



# a LOT of parsing is required to make this work, since it needs to generate command categories etc
help_string = '''
an atrocity made in discord.py by `{", ".join(bot.get_user(i).name + "#" + bot.get_user(i).discriminator for i in DEVELOPER_IDS)}` because I was bored idk

**COMMANDS AVAILABLE:**
'''

for key in help_categorized:
    help_string += f'\n**{key}:**\n\n'
    for name, desc, _ in help_categorized[key]:
        help_string += '— '
        for i in name[:-1]:
            help_string += '`{PREFIX}' + f'{i}`, '
        help_string += '`{PREFIX}' + f'{name[-1]}`: {desc}\n'
help_string += '**\nspecific info for a command can be found by running**```{PREFIX}help <command>```'



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

error_title = 'insert helpful error name here'

error_clampongus = 'you\'re still an absolute clampongus though'