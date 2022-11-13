import config
# I know this should probably be a json file but this is way easier to deal with so cope harder lol

all='''
an atrocity made in discord.py by `{DEVELOPER}` because I was bored idk

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
— `{PREFIX}embed`: like ~say but better
> order of arguments HAS to be `title, description, color (hex), footer`, in a comma separated list. you can omit any of these by providing a space in the comma separated list
> 
> **example: `{PREFIX}embed this is a title, description, , and footer; but no color`**
— `{PREFIX}8ball`, `{PREFIX}ball`: random answers for random questions
— `{PREFIX}rps`: rock paper scissors against spunch bot
— `{PREFIX}crimes`: show all of my crimes
— `{PREFIX}nut`: sacrifice NUT to me''' # can't use an f string since PREFIX can't really be imported easily, instead it's evaluated in main file
