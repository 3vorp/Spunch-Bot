import discord, os, wikipedia, random, json, datetime, dotenv, help_strings, config

dotenv.load_dotenv() # this is so that I don't have the token directly in the file because yeah

try:
    DATABASE = json.loads ( # I'm sorry to whoever has to read this abomination
        open (
            os.path.join (os.path.dirname(__file__), 'database.json'), # gets absolute file path from the relative file path
            'r' # in reading mode
        )
        .read()
    )
except: # gives error if you don't add a database
    print('\033[91m\033[1mERROR: check the README.md more closely:\n\nTL;DR: create a database.json file inside the root folder following the formatting of the database_example.json example file') # that weird stuff at the beginning handles the color
    exit()

DEFAULT_PREFIX = config.DEFAULT_PREFIX
DEVELOPER = config.DEVELOPER
EMBED_COLOR = config.EMBED_COLOR
EMBED_ICON = config.EMBED_ICON
BIG_ICON = config.BIG_ICON
EMBED_GIF = config.EMBED_GIF
BIG_GIF = config.BIG_GIF

TOKEN = os.getenv('TOKEN')

async def write_database(): # I'd be copy and pasting this constantly so this saves me a LOT of time
    with open (os.path.join(os.path.dirname (__file__), 'database.json'), 'w', encoding = 'utf-8') as db: # same thing as reading from the DB
        json.dump ( # allows me to write everything into the json file
            DATABASE,
            db,
            ensure_ascii = False,
            indent = 4
        )
    return # idk if this is necessary but I don't want to mess things up because of the whole async await thing



class Delete_Button(discord.ui.View): # this took me so long to implement please kill me
    def __init__(self):
        super().__init__() # inheritance stuff yes yes I definitely remember stuff from OOP
        
    @discord.ui.button ( # creates a red button object thingy, edit this to edit all delete buttons
        label = 'delete',
        style = discord.ButtonStyle.red
    )
    async def button_clicked(self, interaction:discord.Interaction, button:discord.ui.Button): # whenever button is clicked calls this function
        await interaction.message.delete()



class Main(discord.Client):
    async def on_ready(self): # starts the bot
        STARTUP_CHANNEL = client.get_channel(1034609478005436436) # hardcoded channel ids for a private server, change these if you fork this
        await STARTUP_CHANNEL.send (
            embed = discord.Embed (
                title = f'hello i\'m alive now',
                description = f'```started at {" ".join(datetime.datetime.now().strftime("%c").split())}```', # the redundant .join() and .split() methods removes a really annoying double space
                color = EMBED_COLOR
            )
            .set_footer (
                text = f'Online as {client.user}',
                icon_url = EMBED_ICON
            )
        )
        await client.change_presence(activity = discord.Game('spongeboy gif on repeat')) # discord activity

    async def on_message(self, message):
        if message.author == client.user or message.content == '': # makes sure the bot can't reply to itself and cause an infinite loop
            return

        SUGGEST_CHANNEL = client.get_channel(1035020903953743942) # same as STARTUP_CHANNEL
        try: 
            PREFIX = DATABASE[f'prefix_{message.guild.id}']
        except KeyError: # all of this code essentially just checks if a server prefix already exists, if it does then it uses that, if it doesn't it set it to the DEFAULT_PREFIX
            PREFIX = DEFAULT_PREFIX
        
        SENTENCE = str(message.content).lower() # the .lower() is just used to remove all case sensitivity


        # everything that doesn't need a prefix goes here (mostly the "look for these words and reply to it" messages)


        if 'baller' == SENTENCE:
            await message.reply (
                'https://cdn.discordapp.com/attachments/697947500987809846/1033358086095765504/e923830c4dbe2942417df30bf5530238.mp4',
                view = Delete_Button(),
                mention_author = False
            )

        if 'mhhh' in SENTENCE: # can't use elif because it's checking if it's contained within any of the message contents
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
            )

            await message.channel.send ('smh my head ripping off compli:b:ot very cring') # I basically stole the joke from CompliBot/Faithful Bot so the bot calls you out on it lol
        
        if 'spongeboy' == SENTENCE:
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
        
        if 'hello there' == SENTENCE:
            PROBABILITY = random.randint(0, 5) # special chance for easter egg
            if PROBABILITY == 0:
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
        
        if 'nut' == SENTENCE or f'{PREFIX}nut' == SENTENCE:
            DATABASE['nut_count'] = str(int(DATABASE['nut_count']) + 1) # adds one to the total nut count, type conversions yes yes
            await write_database()
            
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


        elif message.content[0] == PREFIX and message.content[1] != PREFIX: # otherwise it picks up strikethrough which is pain
            WORD_LIST = message.content[1:].lower().split() # removes the prefix and any uppercase, splits contents into list
            COMMAND = WORD_LIST[0] # gets the command portion
            WORD_LIST.pop(0) # removes command from the actual WORD_LIST
            SENTENCE = message.content.partition(' ')[2] # praise stackoverflow, I wanted to keep uppercase but just remove the first word

            # use WORD_LIST for list (lowercase), use SENTENCE for string (exactly as user sent it), use COMMAND for command (literally just the first word)


            # everything that needs a prefix and doesn't require arguments goes here


            if COMMAND == 'rps': # needs to be outside the arguments passed if condition because the bot can automatically provide one if no arguments are passed
                BOT_ANSWER = random.choice(['rock', 'paper', 'scissors']) # works same way as 8ball, randomly chooses from list
                if SENTENCE == '':
                    WORD_LIST = [random.choice(['rock', 'paper', 'scissors'])] # if user provides no arguments it just randomly chooses for them

                if BOT_ANSWER == WORD_LIST[0]: # uses WORD_LIST as opposed to SENTENCE so that if you send multiple arguments it just ignores the rest, also WORD_LIST removes case sensitivity
                    await message.reply (
                        embed = discord.Embed (
                            title = 'it\'s a tie',
                            description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                            color = EMBED_COLOR
                        ),
                        view = Delete_Button(),
                        mention_author = False
                    )

                elif (WORD_LIST[0] == 'scissors' and BOT_ANSWER == 'paper') or (WORD_LIST[0] == 'paper' and BOT_ANSWER == 'rock') or (WORD_LIST[0] == 'rock' and BOT_ANSWER == 'scissors'): # pain
                    await message.reply (
                        embed = discord.Embed (
                            title = 'you win',
                            description = f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                            color = EMBED_COLOR
                        ),
                        view = Delete_Button(),
                        mention_author = False
                    )

                elif (WORD_LIST[0] == 'paper' and BOT_ANSWER == 'scissors') or (WORD_LIST[0] == 'rock' and BOT_ANSWER == 'paper') or (WORD_LIST[0] == 'scissors' and BOT_ANSWER == 'rock'): # pain II
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
            
            elif COMMAND == 'crimes':
                await message.reply (
                    embed = discord.Embed (
                        title = 'officer i drop kicked that child in SELF DEFENSE',
                        description = 'you gotta believe me',
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = 'what do you mean gotta go fast isn\'t a medical condition',
                        icon_url = EMBED_ICON
                    ),
                    view = Delete_Button(),
                    mention_author = False
                )

            elif (COMMAND == 'help' or COMMAND == 'info') and len(WORD_LIST) == 0:
                await message.reply (
                    embed = discord.Embed (
                        title = '**spunch bot**',
                        description = eval(f'f"""{help_strings.all}"""'), # have to convert to f string because help_strings doesn't recognize PREFIX and DEVELOPER as variables
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

            elif len(WORD_LIST) >= 1:



                # every command that requires arguments goes here



                if COMMAND == 'say': # deletes original message and sends the sentence back
                    await message.delete()
                    await message.channel.send(SENTENCE)

                elif COMMAND == 'wikipedia':
                    try:
                        await message.reply ( # this atrocity takes the input, finds a wikipedia article, and trims it to 1900 characters
                            f'```{wikipedia.page(SENTENCE).content[0:1900]}```', # doesn't use embed to save screen space
                            view = Delete_Button(),
                            mention_author = False
                        )

                    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError): # if there's no article with that name catches error and gives info
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

                elif COMMAND == 'suggest' or COMMAND == 'feedback':
                    await SUGGEST_CHANNEL.send ( # sends to hardcoded suggestion channel
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

                elif COMMAND == 'help':
                    flag = False
                    for i in help_strings.help_list: # iterates through the main command list
                        if WORD_LIST[0] in i[0]: # first entry of the list is always the command name(s)
                            await message.reply (
                                embed = discord.Embed (
                                    title = eval(f'f"""{i[1]}"""'), # same reason for eval as the main help command, the [1] is because the second index is always the title
                                    description = eval(f'f"""{i[2]}"""'), # the third index is always the description
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
                                description = f'no command with that name was found, use {PREFIX}help for the full list',
                                color = EMBED_COLOR
                            )
                            .set_footer (
                            text = 'you\'re still an absolute clampongus though',
                            icon_url = EMBED_ICON
                            ),
                            view = Delete_Button(),
                            mention_author = False
                        )

                elif COMMAND == 'prefix' or COMMAND == 'setprefix':
                    if WORD_LIST[0] == 'reset':
                        try:
                            del DATABASE[f'prefix_{message.guild.id}'] # removes value entirely
                            await write_database() # writes the DATABASE dictionary into the actual json file
                            await message.reply (
                                embed = discord.Embed (
                                    title = 'server prefix has been reset',
                                    description = f'default prefix is {DEFAULT_PREFIX}',
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
                        DATABASE[f'prefix_{message.guild.id}'] = f'{SENTENCE[0]}' # writes the prefix to the DATABASE dictionary variable using the guild id as a key
                        await write_database() # writes the DATABASE dictionary into the database.json file
                        await message.reply (
                            embed = discord.Embed (
                                title = f'server prefix changed to {WORD_LIST[0]}',
                                description = f'you can change it back using `{PREFIX}prefix reset`',
                                color = EMBED_COLOR
                            ),
                            view = Delete_Button(),
                            mention_author = False
                        )
                
                elif COMMAND == 'embed':
                    ARG_LIST = SENTENCE.split(',') # uses commas for arguments so you can have spaces in the embed

                    TITLE = ARG_LIST[0]
                    try: # if an argument isn't provided for any of these it just sets it to nothing/defaults
                        DESCRIPTION = ARG_LIST[1]
                    except IndexError: # if an argument isn't provided it raises an IndexError exception, so it will set it to blank instead
                        DESCRIPTION = ''
                    try:
                        COLOR = ARG_LIST[2].strip().lstrip('#') # removes trailing whitespaces because discord.py is VERY picky with hex
                        if COLOR != '': 
                            COLOR = int(COLOR, base=16) # converts into hex number/base 16
                        else: #if no color is provided it would error above rather than just setting it to blank, so we just trigger the except here instead
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
                        .set_footer(text = FOOTER) # no image or thumbnail support yet because I'm too lazy to set up yet more try/excepts, maybe some day lol
                    )
                
                elif COMMAND == 'len' or COMMAND == 'length': # this is a super simple command but tbh it's pretty useful
                    await message.reply (
                        embed = discord.Embed (
                            title = f'Your sentence is {len(SENTENCE)} characters long and {len(WORD_LIST)} words long:',
                            description = f'```{SENTENCE}```',
                            color = EMBED_COLOR
                        ),
                        view = Delete_Button(),
                        mention_author = False
                    )

                else:
                    await message.reply ( # generic error handling
                        embed = discord.Embed (
                            title = 'insert helpful error name here',
                            description = f'too lazy to implement proper errors but you probably sent too much stuff, not enough stuff, or something that\'s not a command\n\n**use `{PREFIX}help` for a list of commands**',
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
                await message.reply ( # generic error handling 2
                    embed = discord.Embed (
                        title = 'insert helpful error name here',
                        description = f'too lazy to implement proper errors but you probably sent too much stuff, not enough stuff, or something that\'s not a command\n\n**use `{PREFIX}help` for a list of commands**',
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = 'you\'re still an absolute clampongus though',
                        icon_url = EMBED_ICON
                    ),
                    view = Delete_Button(),
                    mention_author = False
                )

intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
client = Main(intents = intents)

client.run(TOKEN)