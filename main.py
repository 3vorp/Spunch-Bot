import discord, os, wikipedia, random, json, datetime, dotenv, help_strings, config
intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
client = discord.Client(intents = intents)

dotenv.load_dotenv() # this is so that I don't have the token directly in the file because yeah



### DATABASE ###



try:
    DATABASE = json.loads ( # I'm sorry to whoever has to read this abomination
        open (
            os.path.join ( # gets absolute file path from the relative file path
                os.path.dirname(__file__),
                'database.json'
            ),
            'r' # in reading mode
        )
        .read()
    )

except FileNotFoundError:
    print (help_strings.database_error)
    DATABASE = {} # sets database to empty dictionary if none are found, stops initial errors



### CONST VARIABLES ###



DEFAULT_PREFIX = config.DEFAULT_PREFIX
DEVELOPER = config.DEVELOPER
EMBED_COLOR = config.EMBED_COLOR
EMBED_ICON = config.EMBED_ICON
BIG_ICON = config.BIG_ICON
EMBED_GIF = config.EMBED_GIF
BIG_GIF = config.BIG_GIF

SUGGEST_CHANNEL = config.SUGGEST_CHANNEL
STARTUP_CHANNEL = config.STARTUP_CHANNEL
ANNOUNCEMENT_CHANNEL = config.ANNOUNCEMENT_CHANNEL

TOKEN = os.getenv('TOKEN')



### USEFUL TOOLS ###



async def write_database(): # I'd be copy and pasting this constantly so this saves me a LOT of time
    with open (
        os.path.join (
            os.path.dirname (__file__),
            'database.json'
        ), 
        'w', encoding = 'utf-8'
    ) as db: # same thing as reading from the DB
        json.dump ( # allows me to write everything into the json file
            DATABASE,
            db,
            ensure_ascii = False,
            indent = 4
        )

class Delete_Button(discord.ui.View): # this took me so long to implement please kill me
    def __init__(self):
        super().__init__() # inheritance stuff yes yes I definitely remember stuff from OOP

    @discord.ui.button ( # creates a red button object thingy, edit this to edit all delete buttons
        label = 'delete',
        style = discord.ButtonStyle.red
    )
    async def button_clicked(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.message.delete() # whenever the button is clicked it calls this function



### STARTUP MESSAGE / PRESENCE ###



@client.event
async def on_ready():
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
        ) # redundant .join() and .split() methods to remove an annoying double space
        .set_footer (
            text = f'Online as {client.user}',
            icon_url = EMBED_ICON
        )
    )
    await client.change_presence (
        activity = discord.Game (
            name = 'spongeboy gif on repeat' # sets presence to "playing spongeboy gif on repeat"
        )
    )



@client.event
async def on_message(message):
    if message.author == client.user or message.content == '': return # prevents infinite loops


### PREFIX / ANNOUNCEMENT SHENANIGANS ###


    try: # checks if a server prefix already exists, and sets that as the prefix if it exists
        PREFIX = DATABASE[f'prefix_{message.guild.id}']

    except KeyError: #if there's no server prefix sets it to default prefix
        PREFIX = DEFAULT_PREFIX

    if message.channel.id == ANNOUNCEMENT_CHANNEL:
        for guild in client.guilds:
            channel = guild.text_channels[0] # custom channels coming soon™

            await channel.send (
                embed = discord.Embed (
                    title = f'global announcement from **{message.author}**:',
                    description = message.content,
                    color = EMBED_COLOR
                ),
                view = Delete_Button()
            )

        await message.reply (
            embed = discord.Embed (
                title = 'message pushed to all servers',
                description = f'```{message.content}```',
                color = EMBED_COLOR
            ),
            view = Delete_Button(),
            mention_author = False
        )

    SENTENCE = message.content.lower() # the .lower() is just used to remove all case sensitivity



### GENERAL MESSAGES (mostly the "look for these words and reply/react to it" messages) ###



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
            view = Delete_Button(),
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
            view = Delete_Button(),
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
            view = Delete_Button(),
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
            view = Delete_Button(),
            mention_author = False
        ) # thanks complibot (https://github.com/Faithful-Resource-Pack/Discord-Bot)
        return

    elif SENTENCE == 'nut' or SENTENCE == f'{PREFIX}nut':
        DATABASE['nut_count'] = int(DATABASE['nut_count']) + 1 # adds one to the total nut count
        await write_database() # made a shortcut because it saves a lot of copy+pasting

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
            view = Delete_Button(),
            mention_author = False
        )
        return

### COMMAND HANDLER ###



    if message.content.startswith(PREFIX) == False: return # saves me useless indentation

    WORD_LIST = message.content[len(PREFIX):].lower().split() # general argument list, all lowercase
    COMMAND = WORD_LIST[0] # gets the command itself for convenience
    WORD_LIST.pop(0) # removes command from the actual WORD_LIST, because COMMAND already exists
    SENTENCE = message.content.partition(' ')[2] # removes first word only (praise stackoverflow lol)

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
                view = Delete_Button(),
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
                view = Delete_Button(),
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
                view = Delete_Button(),
                mention_author = False
            )

        else:
            await message.reply (
                embed = discord.Embed (
                    title = 'that wasn\'t an option so I automatically win :sunglasses:',
                    description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                    color = EMBED_COLOR
                ),
                view = Delete_Button(),
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
            view = Delete_Button(),
            mention_author = False
        )
        return

    elif ((COMMAND == 'help' or COMMAND == 'info') and (len(WORD_LIST) == 0 or WORD_LIST[0] == 'all')):
        await message.reply (
            embed = discord.Embed (
                title = '**spunch bot**',
                description = eval(f'f"""{help_strings.all}"""'), # source file can't pass message-specific variables
                color = EMBED_COLOR
            )
            .set_footer (
                text = f'that\'s all for now, go suggest stuff using {PREFIX}feedback if you want me to add stuff ig',
                icon_url = EMBED_ICON
            )
            .set_thumbnail (
                url = BIG_GIF
            ),
            view = Delete_Button(),
            mention_author = False
        )
        return

    elif len(WORD_LIST) < 1: # if a command doesn't have args by this point it probably doesn't exist
        await message.reply (
            embed = discord.Embed (
                title = 'insert helpful error name here',
                description = eval(f'f"""{help_strings.generic_error}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'you\'re still an absolute clampongus though',
                icon_url = EMBED_ICON
            ),
            view = Delete_Button(),
            mention_author = False
        )
        return



### COMMANDS WITH ARGUMENTS ###



    if COMMAND == 'say': # deletes original message and sends the sentence back
        await message.delete()
        await message.channel.send(SENTENCE)
        return

    elif COMMAND == 'wikipedia':
        try:
            await message.reply ( # doesn't use embed to save screen space
                f'```{wikipedia.page(SENTENCE).content[0:1900]}```', # trims to 1900 characters because discord
                view = Delete_Button(),
                mention_author = False
            )

        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError): # basic error handling
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
                view = Delete_Button(),
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
            view = Delete_Button(),
            mention_author = False
        )
        return

    elif COMMAND == 'suggest' or COMMAND == 'feedback':
        await client.get(SUGGEST_CHANNEL).send ( # sends to hardcoded suggestion channel
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
            view = Delete_Button(),
            mention_author = False
        )
        return

    elif COMMAND == 'help' or COMMAND == 'info':
        flag = False
        for i in help_strings.help_list: # iterates through the main command list
            if WORD_LIST[0] in i[0]: # first entry of the list is always the command name(s)
                await message.reply (
                    embed = discord.Embed ( # same reason for using eval() as in the main help command
                        title = eval(f'f"""help for {PREFIX}{i[0][0]}"""'), # gets first value of first index
                        description = eval(f'f"""{i[1]}"""'), # [1] is for getting description
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = f'go suggest stuff using {PREFIX}feedback if you want me to add stuff ig',
                        icon_url = EMBED_ICON
                    )
                    .set_thumbnail (
                        url = BIG_GIF
                    ),
                    view = Delete_Button(),
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
                view = Delete_Button(),
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
                    view = Delete_Button(),
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
                    view = Delete_Button(),
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
                view = Delete_Button(),
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
            view = Delete_Button(),
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
            view = Delete_Button(),
            mention_author = False
        )
        return

    else:
        await message.reply ( # generic error handling
            embed = discord.Embed (
                title = 'insert helpful error name here',
                description = eval(f'f"""{help_strings.generic_error}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'you\'re still an absolute clampongus though',
                icon_url = EMBED_ICON
            ),
            view = Delete_Button(),
            mention_author = False
        )
        return

client.run(TOKEN)