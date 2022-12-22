import discord, os, wikipedia, random, json, datetime, dotenv
from config import *
from help_strings import *
intents = discord.Intents.default() # idk what this does but it looks important so I'm not touching it
intents.message_content = True
client = discord.Client(intents = intents)

deletable = True # global variable for whether to add delete reaction or not



### DATABASE ###



try:
    DATABASE = json.loads ( # I'm sorry to whoever has to read this abomination
        open(os.path.join
            (os.path.dirname(__file__),'database.json'),
            'r'
        )
        .read()
    )

except FileNotFoundError:
    print(database_error) # no eval() necessary because it's not an f string
    DATABASE = {} # sets database to empty dictionary if none are found, stops initial errors



async def write_database(): # saves a LOT of copy paste
    with open (os.path.join
        (os.path.dirname (__file__), 'database.json'),
        'w',
        encoding = 'utf-8'
    ) as db:
        json.dump ( # allows me to write everything into the json file
            DATABASE,
            db,
            ensure_ascii = False,
            indent = 4
        )



### STARTUP MESSAGE / PRESENCE ###



@client.event
async def on_ready():
    global deletable
    deletable = False
    await client.get_channel(STARTUP_CHANNEL).send (
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
            text = f'Online as {client.user}',
            icon_url = EMBED_ICON
        )
    )
    await client.change_presence (
        activity = discord.Game ( # "playing spongeboy gif on repeat"
            name = 'spongeboy gif on repeat'
        )
    )



### DELETE BUTTON / REACTION ###



@client.event # initially had this set up as a button but it only worked on most recent message
async def on_raw_reaction_add(payload): # handles all reacted messages rather than cached ones
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    user = payload.member # compromise for being able to handle all messages is working with raw events :pain:

    if user == client.user: return # detects own reaction and deletes all bot messages otherwise lol

    if reaction.emoji == '🗑️' and message.author == client.user: # only deletes bot messages to prevent abuse
        await message.delete()



@client.event
async def on_message(message):
    global deletable
    if message.author == client.user and deletable == True: # saves a lot of code by applying to every bot message
        await message.add_reaction('🗑️')
        return # nothing else uses bot messages so this stops infinite loops

    else:
        deletable = True

    if message.content == '': return # no point parsing blank messages



### PREFIX / ANNOUNCEMENT SHENANIGANS ###



    try: # assigns server prefix if one exists, if not use default prefix
        PREFIX = DATABASE[f'prefix_{message.guild.id}']

    except KeyError:
        PREFIX = DEFAULT_PREFIX

    if message.channel.id == ANNOUNCEMENT_CHANNEL:
        for guild in client.guilds:
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
        return # you have to use return on basically all commands just to stop canoodling

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

    elif SENTENCE == 'nut' or SENTENCE == f'{PREFIX}nut':
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



### COMMAND HANDLER ###



    if message.content.startswith(PREFIX) == False: return # saves on indentation

    WORD_LIST = message.content[len(PREFIX):].lower().split()
    COMMAND = WORD_LIST[0]
    WORD_LIST.pop(0) # removes command because COMMAND exists now
    SENTENCE = message.content.partition(' ')[2] # praise stackoverflow

    # use WORD_LIST for list (lowercase)
    # use SENTENCE for string (exactly as user sent it)
    # use COMMAND for command (literally just the first word)



### COMMANDS WITHOUT ARGUMENTS ###



    if COMMAND == 'rps':
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
            embed = discord.Embed (
                title = '**spunch bot**',
                description = eval(f'f"""{all}"""'), # source file can't pass message-specific variables
                color = EMBED_COLOR
            )
            .set_footer (
                text = eval(f'f"""{footer}"""'),
                icon_url = EMBED_ICON
            )
            .set_thumbnail (
                url = BIG_GIF
            ),
            mention_author = False
        )
        return

    elif len(WORD_LIST) < 1: # if a command doesn't have args by this point it probably doesn't exist
        await message.reply (
            embed = discord.Embed (
                title = 'insert helpful error name here',
                description = eval(f'f"""{generic_error}"""'),
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
        deletable = False
        await message.delete()
        await message.channel.send(SENTENCE)
        return

    elif COMMAND == 'wikipedia':
        try:
            await message.reply ( # doesn't use embed to save screen space
                f'```{wikipedia.page(SENTENCE).content[0:1900]}```', # trims for character limit
                mention_author = False
            )

        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            await message.reply (
                embed = discord.Embed (
                    title = 'insert helpful error name here',
                    description = 'multiple/no wikipedia article found with that name',
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = 'you\'re still an absolute clampongus though',
                    icon_url = EMBED_ICON
                ),
                mention_author = False
            )
        return

    elif COMMAND == '8ball' or COMMAND == 'ball':
        await message.reply (
            embed = discord.Embed (
                title = SENTENCE,
                description = random.choice ([ # you can add as many options as you want to this list
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
        await client.get_channel(SUGGEST_CHANNEL).send ( # sends to hardcoded suggestion channel
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
                        title = eval(f'f"""help for {PREFIX}{i[0][0]}"""'), # gets first value of first index
                        description = eval(f'f"""{i[1]}"""'), # [1] is for getting description
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = eval(f'f"""{footer}"""'),
                        icon_url = EMBED_ICON
                    )
                    .set_thumbnail (
                        url = BIG_GIF
                    ),
                    mention_author = False
                )

                flag = True
                break # otherwise it's just wasting resources lol

        if flag == False: # there's probably a better way to check if there were no matches but this works too
            await message.reply (
                embed = discord.Embed (
                    title = 'insert helpful error name here',
                    description = f'no command with that name was found, use `{PREFIX}help` for the full list',
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
        if WORD_LIST[0] == 'reset' or SENTENCE == DEFAULT_PREFIX: # checks if changing to default prefix to save space
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
            DATABASE[f'prefix_{message.guild.id}'] = f'{SENTENCE}' # uses guild id as key for easy management
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
        ARG_LIST = SENTENCE.split(',') # uses commas for arguments so you can have spaces in the embed

        TITLE = ARG_LIST[0]
        try: # if an argument isn't provided for any of these it just sets it to nothing/defaults
            DESCRIPTION = ARG_LIST[1]

        except IndexError: # if any argument isn't provided an IndexError is raised, so it just sets it to blank
            DESCRIPTION = ''

        try:
            COLOR = ARG_LIST[2].strip().lstrip('#') # formatting because discord.py is VERY picky with hex
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
        await message.channel.send ( # doesn't use reply so you can't see the original message
            embed = discord.Embed ( # uses all the variables generated in that abomination above to create an embed
                title = TITLE,
                description = DESCRIPTION,
                color = COLOR
            )
            .set_footer(text = FOOTER) # no image or thumbnail support for now because I'm lazy, maybe some day lol
        )
        return

    elif COMMAND == 'len' or COMMAND == 'length': # this is a super simple command but tbh it's pretty useful
        await message.reply (
            embed = discord.Embed (
                title = f'your sentence is {len(SENTENCE)} characters long and {len(WORD_LIST)} words long:',
                description = f'```{SENTENCE}```',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return

    elif COMMAND == 'mock':
        mocked_word = list(SENTENCE.lower()) # separate to WORD_LIST because it's a list of characters not words
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
                description = eval(f'f"""{generic_error}"""'),
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
client.run(os.getenv('TOKEN')) # the actual execution command