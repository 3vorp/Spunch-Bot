import discord, os, wikipedia, random, json, datetime, dotenv
from discord.ext import commands
from config import * # saves me from having to use config.VARIABLE for everything
from help_strings import * # same thing

async def get_prefix(bot, message): # idk why this works but it does
    global PREFIX # so it can be accessed in commands for help embeds etx

    try: # assigns server prefix if one exists, if not use default prefix
        PREFIX = DATABASE[f'prefix_{message.guild.id}']

    except KeyError:
        PREFIX = DEFAULT_PREFIX

    return PREFIX


intents = discord.Intents.default()
intents.message_content = True # special permission required for messages
bot = commands.Bot(intents = intents, command_prefix = get_prefix, case_insensitive=True)
bot.remove_command('help') # default help command is garbage and idk why it's there honestly

deletable = True # global variable for whether to add delete reaction or not



### DATABASE ###



try:
    with open('database.json', 'r') as db:
        DATABASE = json.load(db)

except FileNotFoundError:
    print(error_database) # no eval() necessary because it's not an f string
    DATABASE = {} # stops initial errors, still won't really work though

async def write_database(): # saves a LOT of copy paste
    with open('database.json', 'w') as db:
        json.dump(DATABASE, db, indent = 4, ensure_ascii = False)



### STARTUP MESSAGE / PRESENCE ###



@bot.event
async def on_ready():
    global deletable
    await bot.change_presence (
        activity = discord.Game ( # sends "playing spongeboy gif on repeat"
            name = 'spongeboy gif on repeat'
        )
    )

    deletable = False
    await bot.get_channel(STARTUP_CHANNEL).send (
        embed = discord.Embed (
            title = 'hello i\'m alive now',
            description = f'''```started at {
                ' '.join (
                    datetime.datetime.now().strftime('%c')
                    .split()
                )
            }```''',
            color = EMBED_COLOR
        ) # removes an annoying double space with redundant .join() and .split()
        .set_footer (
            text = f'Online as {bot.user}',
            icon_url = EMBED_GIF
        )
    )




### DELETE BUTTON / REACTION ###



@bot.event
async def on_raw_reaction_add(payload): # using raw events so it works on all bot messages
    user = payload.member
    message = await (
        bot.get_channel(payload.channel_id)
        .fetch_message(payload.message_id)
    )

    if user == bot.user or message.author != bot.user: return # basic checks

    reaction = discord.utils.get ( # boilerplate for variable setup
        message.reactions,
        emoji=payload.emoji.name
    )

    user_list = [] # generates list of people who reacted
    async for i in reaction.users(): # doesn't work unless it's an async for loop, idk why either
        user_list.append(i) # for some reason you can't use reaction.users() but oh well

    if bot.user not in user_list: return # if bot hasn't reacted message is undeletable



    if reaction.emoji == '🗑️': # keeps stuff easily expandable for future
        await message.delete()



@bot.event
async def on_message(message):
    global deletable, PREFIX, bot
    if deletable and message.author == bot.user: # automatically applies by default
        await message.add_reaction('🗑️')
        return # nothing else uses bot messages so this stops infinite loops

    else: # resets the status for the next message
        deletable = True



### GLOBAL ANNOUNCEMENTS ###



    if message.channel.id == ANNOUNCEMENT_CHANNEL:
        for guild in bot.guilds:
            channel = guild.text_channels[0] # custom channels coming soon™

            deletable = False
            await channel.send (
                embed = discord.Embed (
                    title = f'global announcement from **{message.author}**:',
                    description = message.content,
                    color = EMBED_COLOR
                )
            )

        deletable = True
        await message.reply (
            embed = discord.Embed (
                title = 'message pushed to all servers',
                description = f'```{message.content}```',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    SENTENCE = message.content.lower() # removes case sensitivity



### GENERAL/JOKE RESPONSES ###



    if 'f' == SENTENCE: # no match case because less indentation + cleaner aliases
        await message.add_reaction('🇫')
        return # stops canoodling with other commands

    elif 'monke' == SENTENCE:
        await message.add_reaction('🎷')
        await message.add_reaction('🐒')
        return

    elif 'forgor' in SENTENCE: # this way you can have variations like I forgor
        await message.add_reaction('💀')
        return

    elif 'baller' == SENTENCE:
        await message.reply (
            'https://bit.ly/3UY1D0M', # original url was like 130 characters
            mention_author = False
        )
        return

    elif 'spongeboy' == SENTENCE:
        await message.reply (
            embed = discord.Embed (
                color = EMBED_COLOR
            )
            .set_image (
                url = BIG_GIF
            ),
            mention_author = False
        )
        return

    elif 'hello there' == SENTENCE:
        if random.randint(0, 5) == 0: # special chance for easter egg
            url = 'https://i.imgur.com/hAuUsnD.png'

        else:
            url = 'https://media1.tenor.com/images/8dc53503f5a5bb23ef12b2c83a0e1d4d/tenor.gif'

        await message.reply (
            embed = discord.Embed (
                color = EMBED_COLOR
            )
            .set_image (
                url = url
            ),
            mention_author = False
        )
        return

    elif 'mhhh' in SENTENCE: # "mhhh moment" will still count, etc
        await message.reply (
            embed = discord.Embed (
                title = 'mhhh',
                description = '```Uh-oh moment```',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'Swahili → English',
                icon_url = EMBED_GIF
            ),
            mention_author = False
        ) # thanks complibot (https://github.com/Faithful-Resource-Pack/Discord-Bot)
        return

    await bot.process_commands(message)



### UTILITY COMMANDS ###



@bot.command()
async def WIKIPEDIA(ctx, *, SENTENCE): # weird caps because wikipedia is already a library
    try:
        article = wikipedia.page(SENTENCE, pageid = None, auto_suggest = False)
        await ctx.reply (
            embed = discord.Embed (
                title = article.title,
                description = f'**preview:**\n{article.summary}',
                url = article.url,
                color = EMBED_COLOR
            )
            .set_thumbnail (
                url = 'https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png'
            ),
            mention_author = False
        )
    except wikipedia.exceptions.PageError:
        await ctx.reply (
            embed = discord.Embed (
                title = 'insert helpful error name here',
                description = f'no wikipedia article called "{SENTENCE}" was found',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'you\'re still an absolute clampongus though',
                icon_url = EMBED_GIF
            ),
            mention_author = False
        )

    except wikipedia.exceptions.DisambiguationError as error:
        final = '' # don't ask why I spent this much time formatting the list
        for i in range(len(error.options)-1):
            final += f'{error.options[i].lower()}, '
        final += f'and {error.options[-1].lower()}'

        await ctx.reply (
            embed = discord.Embed (
                title = 'multiple options found:',
                description = f'{final} are all possible options',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'be more specific',
                icon_url = EMBED_GIF
            ),
            mention_author = False
        )



@bot.command(aliases=['suggest'])
async def feedback(ctx, *, SENTENCE):
    global deletable
    deletable = False
    await bot.get_channel(SUGGEST_CHANNEL).send ( # edit this channel in config.py
        embed = discord.Embed (
            title = f'feedback sent by **{ctx.author}**:',
            description = f'sent in {ctx.channel.mention}: ```{SENTENCE}```',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'idk maybe react to this if you complete it or something',
            icon_url = EMBED_GIF
        )
    )

    deletable = True
    await ctx.reply ( # sends confirmation message to user
        embed = discord.Embed (
            title = 'your feedback has been sent:',
            description = f'```{SENTENCE}```',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'in the meantime idk go touch grass',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )



@bot.command(aliases=['prefix'])
async def setprefix(ctx, *, SENTENCE):
    if SENTENCE == 'reset' or DEFAULT_PREFIX == SENTENCE:
        try:
            del DATABASE[f'prefix_{ctx.guild.id}'] # removes value entirely
            await write_database() # writes the DATABASE dictionary into the actual json file
            await ctx.reply (
                embed = discord.Embed (
                    title = 'server prefix has been reset',
                    description = f'default prefix is `{DEFAULT_PREFIX}`',
                    color = EMBED_COLOR
                ),
                mention_author = False
            )

        except KeyError:
            await ctx.reply (
                embed = discord.Embed (
                    title = 'insert helpful error name here',
                    description = 'there was no prefix set for this server',
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = 'you\'re still an absolute clampongus though',
                    icon_url = EMBED_GIF
                ),
                mention_author = False
            )
        return

    DATABASE[f'prefix_{ctx.guild.id}'] = f'{SENTENCE}' # convenient to use guild id as key
    await write_database() # writes the DATABASE dictionary into the database.json file
    await ctx.reply (
        embed = discord.Embed (
            title = f'server prefix changed to {SENTENCE}',
            description = f'you can change it back using `{SENTENCE}prefix reset`',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'this was painful to implement so you better appreciate it',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )



@bot.command(aliases=['len'])
async def length(ctx, *, SENTENCE):
    WORD_LIST = SENTENCE.split() # you need both word list and sentence

    if len(SENTENCE) == 1: # grammar stuff because I'm a perfectionist lol
        character = 'character'
    else: character = 'characters'

    if len(WORD_LIST) == 1:
        word = 'word'
    else: word = 'words'

    await ctx.reply (
        embed = discord.Embed (
            title = f'your sentence is {len(SENTENCE)} {character} long and {len(WORD_LIST)} {word} long:',
            description = f'```{SENTENCE}```',
            color = EMBED_COLOR
        ),
        mention_author = False
    )



@bot.command()
async def github(ctx):
    await ctx.reply (
        embed = discord.Embed (
            title = 'you can find my code on github here:',
            description = 'https://github.com/3vorp/Spunch-Bot',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'fair warning that it\'s is a dumpster fire to read through',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )



@bot.command(aliases=['info'])
async def help(ctx, *WORD_LIST):
    if len(WORD_LIST) < 1 or 'all' in WORD_LIST: # can't use indexes if it doesn't exist
        await ctx.reply (
            embed = discord.Embed ( # passed variables need to be evaluated per-message
                title = '**spunch bot**',
                description = eval(f'f"""{help_all}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = eval(f'f"""{help_footer}"""'),
                icon_url = EMBED_GIF
            )
            .set_thumbnail (
                url = BIG_GIF
            ),
            mention_author = False
        )
        return

    for i in help_list: # iterates through the main command list
        if WORD_LIST[0] in i[0]: # first entry of the list is always the command name(s)
            await ctx.reply (
                embed = discord.Embed ( # same reason for using eval() as in the main help command
                    title = eval(f'f"""help for {PREFIX}{i[0][0]}"""'), # grabs first entry from tuple
                    description = eval(f'f"""{i[1]}"""'), # grabs second entry from list (description)
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = eval(f'f"""{help_footer}"""'),
                    icon_url = EMBED_GIF
                )
                .set_thumbnail (
                    url = BIG_GIF
                ),
                mention_author = False
            )
            return # only needs to check for one match and then it's done

    await ctx.reply (
        embed = discord.Embed (
            title = 'insert helpful error name here',
            description = eval(f'f"""{help_not_found}"""'),
            color = EMBED_COLOR
        )
        .set_footer (
        text = 'you\'re still an absolute clampongus though',
        icon_url = EMBED_GIF
        ),
        mention_author = False
    )



### FUN COMMANDS ###



@bot.command()
async def say(ctx, *, SENTENCE):
    global deletable # has to be declared global in every single command that uses it
    await ctx.message.delete()

    deletable = False
    await ctx.channel.send(SENTENCE)



@bot.command()
async def EMBED(ctx, *, SENTENCE): # same as wikipedia
    global deletable
    ARG_LIST = SENTENCE.split(';') # so you can have spaces in the embed

    if ARG_LIST[0].startswith('https://') or ARG_LIST[0].startswith('http://'):
        IMAGE = ARG_LIST[0] # this way you can have image embeds and titles
        TITLE = None
    else:
        TITLE = ARG_LIST[0]
        IMAGE = None

    try: # just sets it to nothing/defaults if nothing is specified
        DESCRIPTION = ARG_LIST[1]
    except IndexError: # passes into except clause if any argument isn't provided
        DESCRIPTION = ''

    try:
        COLOR = ARG_LIST[2].strip().lstrip('#') # discord.py is VERY picky with hex
        if COLOR: # if not empty
            COLOR = int(COLOR, base=16) # converts into hex number/base 16
        else: # trigger the except if no color is provided
            raise IndexError
    except (IndexError, ValueError): # also catches invalid colors
        COLOR = EMBED_COLOR

    try:
        FOOTER = ARG_LIST[3]
    except IndexError:
        FOOTER = ''

    try:
        FOOTER_IMAGE = ARG_LIST[4]
    except IndexError:
        FOOTER_IMAGE = None

    try:
        THUMBNAIL = ARG_LIST[5]
    except IndexError:
        THUMBNAIL = None

    await ctx.message.delete()

    deletable = False
    await ctx.channel.send ( # deletes original message so doesn't use reply
        embed = discord.Embed ( # compiles all variables from above into one embed
            title = TITLE,
            description = DESCRIPTION,
            color = COLOR
        )
        .set_footer (
            text = FOOTER,
            icon_url = FOOTER_IMAGE
        )
        .set_thumbnail (
            url = THUMBNAIL
        )
        .set_image (
            url = IMAGE
        )
    )



@bot.command(aliases=['8ball'])
async def ball(ctx, *, SENTENCE):
    await ctx.reply (
        embed = discord.Embed (
            title = SENTENCE,
            description = random.choice ([ # infinitely expandable list
                'yes',
                'no',
                'maybe',
                'idk',
                'ask later',
                'definitely',
                'never',
                'never ask me that again'
            ]),
            color = EMBED_COLOR
        ),
        mention_author = False
    )




@bot.command(aliases=['roll'])
async def dice(ctx, *WORD_LIST: int): # cast to int to use range() and random() later on
    WORD_LIST = list(WORD_LIST) # converting from tuple to be able to use .append() later on

    if len(WORD_LIST) < 1:
        WORD_LIST = [1,6]

    try: WORD_LIST[1] # if you provide number but not sides

    except IndexError:
        WORD_LIST.append(6) # generates args if user doesn't provide any

    final = 0
    for _ in range(WORD_LIST[0]):
        rolled = random.randint(1, WORD_LIST[1])
        final += rolled # adds new amount to already existing amount

    await ctx.reply (
        embed = discord.Embed (
            title = f'you rolled a {final}',
            description = f'using {WORD_LIST[0]} {WORD_LIST[1]}-sided dice',
            color = EMBED_COLOR
        ),
        mention_author = False
    )



@bot.command()
async def mock(ctx, *, SENTENCE):
    mocked_word = list(SENTENCE.lower()) # list of characters rather than words
    for i in range(len(mocked_word)):
        if i % 2 == 0:
            mocked_word[i] = mocked_word[i].upper()

    await ctx.reply (
        embed = discord.Embed (
            title = 'imagine mocking other users over the internet couldn\'t be me',
            description = f'```{"".join(mocked_word)}```',
            color = EMBED_COLOR
        ),
        mention_author = False
    )



@bot.command()
async def rps(ctx, *WORD_LIST):
    BOT_ANSWER = random.choice(['rock', 'paper', 'scissors'])

    if len(WORD_LIST) < 1: # if user provides no choice bot chooses for them
        WORD_LIST = [random.choice(['rock', 'paper', 'scissors'])]

    if BOT_ANSWER == WORD_LIST[0]:
        await ctx.reply (
            embed = discord.Embed (
                title = 'it\'s a tie',
                description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    elif ( # pain
        (WORD_LIST[0] == 'scissors' and BOT_ANSWER == 'paper') or
        (WORD_LIST[0] == 'paper' and BOT_ANSWER == 'rock') or
        (WORD_LIST[0] == 'rock' and BOT_ANSWER == 'scissors')
    ):
        await ctx.reply (
            embed = discord.Embed (
                title = 'you win',
                description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    elif ( # pain II
        (WORD_LIST[0] == 'paper' and BOT_ANSWER == 'scissors') or
        (WORD_LIST[0] == 'rock' and BOT_ANSWER == 'paper') or
        (WORD_LIST[0] == 'scissors' and BOT_ANSWER == 'rock')
    ):
        await ctx.reply (
            embed = discord.Embed (
                title = 'i win',
                description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    else:
        await ctx.reply (
            embed = discord.Embed (
                title = 'that wasn\'t an option so I automatically win :sunglasses:',
                description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )



@bot.command()
async def nut(ctx, *, SENTENCE=None):
    if SENTENCE == 'total':
        await ctx.reply (
            embed = discord.Embed (
                title = f'total amount of NUT: **{DATABASE["nut_count"]}**',
                description = 'all fine additions to my collection',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return # fancy guard clause, saves indentation so I use these everywhere

    DATABASE['nut_count'] = int(DATABASE['nut_count']) + 1
    await write_database() # adds one to global nut count and writes it

    if DATABASE["nut_count"] % 50 == 0: # special NUT
        await ctx.reply (
            embed = discord.Embed (
                title = 'you have sacrificed a special NUT',
                description = f'you have provided the lucky {DATABASE["nut_count"]}th NUT to my collection',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'i\'m literally just checking for multiples of 50 lol',
                icon_url = EMBED_GIF
            ),
            mention_author = False
        )
        return

    await ctx.reply (
        embed = discord.Embed (
            title = 'you have sacrificed NUT',
            description = 'this will make a fine addition to my collection',
            color = EMBED_COLOR
        )
        .set_footer (
            text = f'total nuts collected: {DATABASE["nut_count"]}',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )


@bot.event
async def on_command_error(ctx, error):
    await ctx.reply ( # generic error handling
        embed = discord.Embed (
            title = 'insert helpful error name here',
            description = eval(f'f"""{error_generic}"""'),
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'you\'re still an absolute clampongus though',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )

dotenv.load_dotenv() # stops token from being in public files
bot.run(os.getenv('TOKEN')) # the actual execution command