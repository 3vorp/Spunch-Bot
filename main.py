import discord, os, wikipedia, random, json, datetime, dotenv
from config import * # saves me from having to use config.VARIABLE for everything
from help_strings import * # same thing

intents = discord.Intents.default()
intents.message_content = True # special permission required for messages
bot = discord.Client(intents = intents) # creating the actual bot client

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
        json.dump(DATABASE, db, ensure_ascii = False, indent = 4)



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
            title = f'hello i\'m alive now',
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
            icon_url = EMBED_ICON
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

    reaction = discord.utils.get (
        message.reactions, emoji=payload.emoji.name
    ) # boilerplate since its handing raw events



    if user == bot.user or message.author != bot.user: return # stops abuse/infinite loops

    if reaction.emoji == '🗑️': # keeps stuff easily expandable for future
        await message.delete()



@bot.event
async def on_message(message):
    global deletable
    if deletable and message.author == bot.user: # automatically applies by default
        await message.add_reaction('🗑️')
        return # nothing else uses bot messages so this stops infinite loops

    else: # resets the status for the next message
        deletable = True

    if message.content == '': return # no point parsing blank messages



### GLOBAL ANNOUNCEMENTS ###



    if message.channel.id == ANNOUNCEMENT_CHANNEL:
        for guild in bot.guilds:
            channel = guild.text_channels[0] # custom channels coming soon™

            await channel.send (
                embed = discord.Embed (
                    title = f'global announcement from **{message.author}**:',
                    description = message.content,
                    color = EMBED_COLOR
                )
            )

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



    if SENTENCE == 'f':
        await message.add_reaction('🇫')
        return # stops canoodling with other commands

    elif SENTENCE == 'monke':
        await message.add_reaction('🎷')
        await message.add_reaction('🐒')
        return

    elif 'forgor' in SENTENCE:
        await message.add_reaction('💀')
        return

    elif SENTENCE == 'baller':
        await message.reply (
            'https://bit.ly/3UY1D0M', # original url was like 130 characters
            mention_author = False
        )
        return

    elif SENTENCE == 'spongeboy':
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

    elif SENTENCE == 'hello there':
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

    elif 'mhhh' in SENTENCE:
        await message.reply (
            embed = discord.Embed (
                title = 'mhhh',
                description = '```Uh-oh moment```',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'Swahili → English',
                icon_url = EMBED_ICON
            ),
            mention_author = False
        ) # thanks complibot (https://github.com/Faithful-Resource-Pack/Discord-Bot)
        return



### COMMAND HANDLER ###



    try: # assigns server prefix if one exists, if not use default prefix
        PREFIX = DATABASE[f'prefix_{message.guild.id}']

    except KeyError:
        PREFIX = DEFAULT_PREFIX

    if not message.content.startswith(PREFIX): return # saves on indentation

    WORD_LIST = message.content[len(PREFIX):].lower().split()
    COMMAND = WORD_LIST[0]
    WORD_LIST.pop(0) # removes command because COMMAND exists now
    SENTENCE = message.content.partition(' ')[2] # removes command but keeps whitespace

    # use WORD_LIST for list (lowercase)
    # use SENTENCE for string (exactly as user sent it)
    # use COMMAND for command (literally just the first word)



### COMMANDS WITH OPTIONAL / NO ARGUMENTS ###



    if COMMAND == 'nut':
        if WORD_LIST[0] == 'total' or WORD_LIST[0] == 'amount':
            await message.reply (
                embed = discord.Embed (
                    title = f'total amount of NUT: **{DATABASE["nut_count"]}**',
                    description = 'all fine additions to my collection',
                    color = EMBED_COLOR
                ),
                mention_author = False
            )

        else: # this way you can provide anything besides keywords and it still adds
            DATABASE['nut_count'] = int(DATABASE['nut_count']) + 1
            await write_database() # adds one to global nut count and writes it

            await message.reply (
                embed = discord.Embed (
                    title = 'you have sacrificed NUT',
                    description = 'this will make a fine addition to my collection',
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = f'total nuts collected: {DATABASE["nut_count"]}',
                    icon_url = EMBED_ICON
                ),
                mention_author = False
            )
        return

    elif COMMAND == 'rps':
        BOT_ANSWER = random.choice(['rock', 'paper', 'scissors'])

        if SENTENCE == '': # if user provides no choice bot chooses for them
            WORD_LIST = [random.choice(['rock', 'paper', 'scissors'])]

        if BOT_ANSWER == WORD_LIST[0]:
            await message.reply (
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
            await message.reply (
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
            await message.reply (
                embed = discord.Embed (
                    title = 'i win',
                    description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                    color = EMBED_COLOR
                ),
                mention_author = False
            )

        else:
            await message.reply (
                embed = discord.Embed (
                    title = 'that wasn\'t an option so I automatically win :sunglasses:',
                    description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                    color = EMBED_COLOR
                ),
                mention_author = False
            )
        return

    elif COMMAND == 'dice' or COMMAND == 'roll': # [0] is how many, [1] is sides
        if SENTENCE == '':
            WORD_LIST = ['1','6']

        try: # if you provide number but not sides
            WORD_LIST[1] # literally just tries seeing if it exists

        except IndexError:
            WORD_LIST.append('6') # generates args if user doesn't provide any

        final = 0
        for i in range(int(WORD_LIST[0])): # int() because message.content is a string
            rolled = random.randint(1, int(WORD_LIST[1]))
            final += rolled # adds new amount to already existing amount

        await message.reply (
            embed = discord.Embed (
                title = f'you rolled a {final}',
                description = f'using {WORD_LIST[0]} {WORD_LIST[1]}-sided dice',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return

    elif COMMAND == 'github':
        await message.reply (
            embed = discord.Embed (
                title = 'you can find my code on github here:',
                description = 'https://github.com/3vorp/Spunch-Bot',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'fair warning that it\'s is a dumpster fire to read through',
                icon_url = EMBED_ICON
            ),
            mention_author = False
        )
        return

    elif (
        (COMMAND == 'help' or COMMAND == 'info') and
        (len(WORD_LIST) == 0 or WORD_LIST[0] == 'all')
    ):
        await message.reply (
            embed = discord.Embed ( # passed variables need to be evaluated per-message
                title = '**spunch bot**',
                description = eval(f'f"""{help_all}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = eval(f'f"""{help_footer}"""'),
                icon_url = EMBED_ICON
            )
            .set_thumbnail (
                url = BIG_GIF
            ),
            mention_author = False
        )
        return

    elif len(WORD_LIST) < 1: # basically just a fancy guard clause
        await message.reply (
            embed = discord.Embed (
                title = 'insert helpful error name here',
                description = eval(f'f"""{error_generic}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'you\'re still an absolute clampongus though',
                icon_url = EMBED_ICON
            ),
            mention_author = False
        )
        return



### COMMANDS WITH ARGUMENTS ###



    if COMMAND == 'say': # deletes original message and sends the sentence back
        await message.delete()

        deletable = False
        await message.channel.send(SENTENCE)
        return

    elif COMMAND == 'wikipedia':
        try:
            await message.reply ( # doesn't use embed to save screen space
                f'```{wikipedia.page(SENTENCE, pageid = None, auto_suggest = False).content[0:1994]}```',
                mention_author = False
            )

        except wikipedia.exceptions.PageError:
            await message.reply (
                embed = discord.Embed (
                    title = 'insert helpful error name here',
                    description = 'no wikipedia article found with that name',
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = 'you\'re still an absolute clampongus though',
                    icon_url = EMBED_ICON
                ),
                mention_author = False
            )

        except wikipedia.exceptions.DisambiguationError as error:
            CHOICE = random.choice(error.options) # if multiple pages are found picks random one
            await message.reply (
                f'```{wikipedia.page(CHOICE, pageid = None, auto_suggest = False).content[0:1994]}```',
                mention_author = False
            )
        return

    elif COMMAND == '8ball' or COMMAND == 'ball':
        await message.reply (
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
        return

    elif COMMAND == 'suggest' or COMMAND == 'feedback':
        deletable = False
        await bot.get_channel(SUGGEST_CHANNEL).send ( # edit this channel in config.py
            embed = discord.Embed (
                title = f'feedback sent by **{message.author}**:',
                description = f'sent in {message.channel.mention}: ```{SENTENCE}```',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'idk maybe react to this if you complete it or something',
                icon_url = EMBED_ICON
            )
        )

        deletable = True
        await message.reply ( # sends confirmation message to user
            embed = discord.Embed (
                title = f'your feedback has been sent to {DEVELOPER}:',
                description = f'```{SENTENCE}```',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'in the meantime idk go touch grass',
                icon_url = EMBED_ICON
            ),
            mention_author = False
        )
        return

    elif COMMAND == 'help' or COMMAND == 'info':
        flag = False
        for i in help_list: # iterates through the main command list
            if WORD_LIST[0] in i[0]: # first entry of the list is always the command name(s)
                await message.reply (
                    embed = discord.Embed ( # same reason for using eval() as in the main help command
                        title = eval(f'f"""help for {PREFIX}{i[0][0]}"""'), # grabs first entry from tuple
                        description = eval(f'f"""{i[1]}"""'), # grabs second entry from list (description)
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = eval(f'f"""{help_footer}"""'),
                        icon_url = EMBED_ICON
                    )
                    .set_thumbnail (
                        url = BIG_GIF
                    ),
                    mention_author = False
                )

                flag = True
                break # only needs to check for one match, otherwise just wasting resources lol

        if not flag: # there's probably an easier way to do this but oh well
            await message.reply (
                embed = discord.Embed (
                    title = 'insert helpful error name here',
                    description = eval(f'f"""{help_not_found}"""'),
                    color = EMBED_COLOR
                )
                .set_footer (
                text = 'you\'re still an absolute clampongus though',
                icon_url = EMBED_ICON
                ),
                mention_author = False
            )
        return

    elif COMMAND == 'prefix' or COMMAND == 'setprefix':
        if WORD_LIST[0] == 'reset' or SENTENCE == DEFAULT_PREFIX: # no point having defaults saved in DB
            try:
                del DATABASE[f'prefix_{message.guild.id}'] # removes value entirely
                await write_database() # writes the DATABASE dictionary into the actual json file
                await message.reply (
                    embed = discord.Embed (
                        title = 'server prefix has been reset',
                        description = f'default prefix is `{DEFAULT_PREFIX}`',
                        color = EMBED_COLOR
                    ),
                    mention_author = False
                )

            except KeyError:
                await message.reply (
                    embed = discord.Embed (
                        title = 'insert helpful error name here',
                        description = 'there was no prefix set for this server',
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = 'you\'re still an absolute clampongus though',
                        icon_url = EMBED_ICON
                    ),
                    mention_author = False
                )

        else:
            DATABASE[f'prefix_{message.guild.id}'] = f'{SENTENCE}' # convenient to use guild id as key
            await write_database() # writes the DATABASE dictionary into the database.json file
            await message.reply (
                embed = discord.Embed (
                    title = f'server prefix changed to {SENTENCE}',
                    description = f'you can change it back using `{SENTENCE}prefix reset`',
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = 'this took me a long time to add so you better appreciate it',
                    icon_url = EMBED_ICON
                ),
                mention_author = False
            )
        return

    elif COMMAND == 'embed':
        ARG_LIST = SENTENCE.split(',') # so you can have spaces in the embed

        TITLE = ARG_LIST[0]
        try: # just sets it to nothing/defaults if nothing is specified
            DESCRIPTION = ARG_LIST[1]

        except IndexError: # passes into except clause if any argument isn't provided
            DESCRIPTION = ''

        try:
            COLOR = ARG_LIST[2].strip().lstrip('#') # discord.py is VERY picky with hex codes
            if COLOR != '':
                COLOR = int(COLOR, base=16) # converts into hex number/base 16

            else: # trigger the except if no color is provided
                raise IndexError

        except IndexError:
            COLOR = EMBED_COLOR

        try:
            FOOTER = ARG_LIST[3]

        except IndexError:
            FOOTER = ''

        await message.delete()

        deletable = False
        await message.channel.send ( # deletes original message so doesn't use reply
            embed = discord.Embed ( # compiles all variables from above into one embed
                title = TITLE,
                description = DESCRIPTION,
                color = COLOR
            )
            .set_footer(text = FOOTER) # no image or thumbnail support for now, too lazy
        )
        return

    elif COMMAND == 'len' or COMMAND == 'length': # simple but tbh kinda useful
        if len(SENTENCE) == 1: # grammar stuff because I'm a perfectionist lol
            character = 'character'
        else: character = 'characters'

        if len(WORD_LIST) == 1:
            word = 'word'
        else: word = 'words'

        await message.reply (
            embed = discord.Embed (
                title = f'your sentence is {len(SENTENCE)} {character} long and {len(WORD_LIST)} {word} long:',
                description = f'```{SENTENCE}```',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return

    elif COMMAND == 'mock':
        mocked_word = list(SENTENCE.lower()) # list of characters rather than words
        for i in range(len(mocked_word)):
            if i % 2 == 0:
                mocked_word[i] = mocked_word[i].upper()

        await message.reply (
            embed = discord.Embed (
                title = 'imagine mocking other users over the internet couldn\'t be me',
                description = f'```{"".join(mocked_word)}```',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return

    else:
        await message.reply ( # generic error handling
            embed = discord.Embed (
                title = 'insert helpful error name here',
                description = eval(f'f"""{error_generic}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'you\'re still an absolute clampongus though',
                icon_url = EMBED_ICON
            ),
            mention_author = False
        )
        return

dotenv.load_dotenv() # stops token from being in public files
bot.run(os.getenv('TOKEN')) # the actual execution command