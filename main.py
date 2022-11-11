import discord, os, wikipedia, random, json
from datetime import datetime # used for startup message
from dotenv import load_dotenv # this is so that I don't have the token directly in the file because yeah
load_dotenv()

DATABASE = json.loads ( # I'm sorry to whoever has to read this abomination
    open (
        os.path.join (os.path.dirname(__file__), 'database.json'), # gets absolute file path from the relative file path
        'r' # in reading mode
    )
    .read()
)

DEVELOPER = 'Evorp#5819' # idk why I included this here but who cares honestly
EMBED_COLOR = 0xc3ba5c # this is just a hex color code (#C3BA5C) with 0x in front of it so discord parses it as hex, idk why either
EMBED_ICON = 'https://raw.githubusercontent.com/3vorp/Spunch-Bot/main/assets/embed_icon.png' # frame 106 of the spongeboy gif, probably some better way to get the icon but this works too :P
BIG_ICON = 'https://raw.githubusercontent.com/3vorp/Spunch-Bot/main/assets/big_icon.png'
EMBED_GIF = 'https://raw.githubusercontent.com/3vorp/Spunch-Bot/main/assets/embed_icon.gif'
BIG_GIF = 'https://raw.githubusercontent.com/3vorp/Spunch-Bot/main/assets/big_icon.gif'

TOKEN = os.getenv('TOKEN')

async def write_database(): # I'd be copy and pasting this constantly so this saves me a LOT of time
    with open (os.path.join(os.path.dirname (__file__), 'database.json'), 'w', encoding='utf-8') as db: # same thing as reading from the DB
        json.dump( # allows me to write everything into the json file
            DATABASE,
            db,
            ensure_ascii=False,
            indent=4
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
                description=f'```started at {" ".join(datetime.now().strftime("%c").split( ))}```', # the redundant .join() and .split( ) methods removes a really annoying double space
                color = EMBED_COLOR
            )
            .set_footer (
                text=f'Online as {client.user}',
                icon_url=EMBED_ICON
            )
        )
        await client.change_presence(activity=discord.Game('spongeboy gif on repeat')) # discord activity

    async def on_message(self, message):
        if message.author == client.user or message.content == '': # makes sure the bot can't reply to itself and cause an infinite loop
            return

        SUGGEST_CHANNEL = client.get_channel(1035020903953743942) # same as STARTUP_CHANNEL
        try: 
            PREFIX = DATABASE[f'prefix_{message.guild.id}']
        except KeyError: # if there's no custom prefix set it just uses ~ as the default, change this if you want to change all prefixes
            PREFIX = '~'
        
        SENTENCE = str(message.content).lower() # the .lower() is just used to remove all case sensitivity


        # everything that doesn't need a prefix goes here (mostly the "look for these words and reply to it" messages)


        if 'baller' == SENTENCE:
            await message.reply (
                'https://cdn.discordapp.com/attachments/697947500987809846/1033358086095765504/e923830c4dbe2942417df30bf5530238.mp4',
                view=Delete_Button(),
                mention_author=False
            )

        if 'mhhh' in SENTENCE: # can't use elif because it's checking if it's contained within any of the message contents
            await message.reply (
                embed = discord.Embed (
                    title='mhhh',
                    description='```Uh-oh moment```',
                    color = EMBED_COLOR
                )
                .set_footer (
                    text='Swahili → English',
                    icon_url=EMBED_ICON
                ),
                view=Delete_Button(),
                mention_author=False
            )

            await message.channel.send ('smh my head ripping off compli:b:ot very cring') # I basically stole the joke from CompliBot/Faithful Bot so the bot calls you out on it lol
        
        if 'spongeboy' == SENTENCE:
            await message.reply (
                embed=discord.Embed (
                    color=EMBED_COLOR
                )
                .set_image (
                    url=BIG_GIF
                ),
                view = Delete_Button(),
                mention_author=False
            )
        
        if 'hello there' == SENTENCE:
            PROBABILITY = random.randint(0, 5) # special chance for easter egg
            if PROBABILITY == 0:
                url = 'https://i.imgur.com/hAuUsnD.png'
            else:
                url = 'https://media1.tenor.com/images/8dc53503f5a5bb23ef12b2c83a0e1d4d/tenor.gif'

            await message.reply (
                embed=discord.Embed (
                    color=EMBED_COLOR
                )
                .set_image (
                    url=url
                ),
                view=Delete_Button(),
                mention_author=False
            )
        
        if 'nut' == SENTENCE or f'{PREFIX}nut' == SENTENCE:
            DATABASE['nut_count'] = str(int(DATABASE['nut_count']) + 1) # adds one to the total nut count, type conversions yes yes
            await write_database()
            
            await message.reply (
                embed=discord.Embed (
                    title='you have sacrificed NUT',
                    description='this will make a fine addition to my collection',
                    color=EMBED_COLOR
                )
                .set_footer (
                    text=f'total nuts collected: {DATABASE["nut_count"]}',
                    icon_url=EMBED_ICON
                ),
                view=Delete_Button(),
                mention_author=False
            )


        elif message.content[0] == PREFIX and message.content[1] != PREFIX: # otherwise it picks up strikethrough which is pain
            WORD_LIST=message.content[1:].lower().split( ) # removes the prefix and any uppercase, splits contents into list
            COMMAND=WORD_LIST[0] # gets the command portion
            WORD_LIST.pop(0) # removes command from the actual WORD_LIST
            SENTENCE=message.content.partition(' ')[2] # praise stackoverflow, I wanted to keep uppercase but just remove the first word

            # use WORD_LIST for list (lowercase), use SENTENCE for string (exactly as user sent it), use COMMAND for command (literally just the first word)


            # everything that needs a prefix and doesn't require arguments goes here


            if COMMAND == 'rps': # needs to be outside the arguments passed if condition because the bot can automatically provide one if no arguments are passed
                BOT_ANSWER=random.choice(['rock', 'paper', 'scissors']) # works same way as 8ball, randomly chooses from list
                if SENTENCE == '':
                    WORD_LIST = [random.choice(['rock', 'paper', 'scissors'])] # if user provides no arguments it just randomly chooses for them

                if BOT_ANSWER == WORD_LIST[0]: # uses WORD_LIST as opposed to SENTENCE so that if you send multiple arguments it just ignores the rest, also WORD_LIST removes case sensitivity
                    await message.reply (
                        embed = discord.Embed (
                            title = 'it\'s a tie',
                            description=f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                            color=EMBED_COLOR
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )

                elif (WORD_LIST[0] == 'scissors' and BOT_ANSWER == 'paper') or (WORD_LIST[0] == 'paper' and BOT_ANSWER == 'rock') or (WORD_LIST[0] == 'rock' and BOT_ANSWER == 'scissors'): # pain
                    await message.reply (
                        embed = discord.Embed (
                            title = 'you win',
                            description=f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                            color=EMBED_COLOR
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )

                elif (WORD_LIST[0] == 'paper' and BOT_ANSWER == 'scissors') or (WORD_LIST[0] == 'rock' and BOT_ANSWER == 'paper') or (WORD_LIST[0] == 'scissors' and BOT_ANSWER == 'rock'): # pain II
                    await message.reply (
                        embed = discord.Embed (
                            title= 'i win',
                            description=f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                            color=EMBED_COLOR
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )

                else:
                    await message.reply (
                        embed = discord.Embed (
                            title='that wasn\'t an option so I automatically win :sunglasses:',
                            description=f'you sent {WORD_LIST[0]}, i sent {BOT_ANSWER}',
                            color=EMBED_COLOR
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )
            
            elif COMMAND == 'github':
                await message.reply (
                    embed=discord.Embed (
                        title='you can find my code on github here:',
                        description='https://github.com/3vorp/Spunch-Bot',
                        color=EMBED_COLOR
                    )
                    .set_footer (
                        text='fair warning that it\'s is a dumpster fire to read through',
                        icon_url=EMBED_ICON
                    ),
                    view=Delete_Button(),
                    mention_author=False
                )
            
            elif COMMAND == 'crimes':
                await message.reply (
                    embed=discord.Embed (
                        title='officer i drop kicked that child in SELF DEFENSE',
                        description='you gotta believe me',
                        color=EMBED_COLOR
                    )
                    .set_footer (
                        text='what do you mean gotta go fast isn\'t a medical condition',
                        icon_url=EMBED_ICON
                    ),
                    view=Delete_Button(),
                    mention_author=False
                )

            elif (COMMAND == 'help' or COMMAND == 'info') and len(WORD_LIST) == 0:
                await message.reply (
                    embed = discord.Embed (
                        title = '**spunch bot**',
                        description = f''' 
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
— `{PREFIX}8ball`, `{PREFIX}ball`: random answers for random questions
— `{PREFIX}rps`: rock paper scissors against spunch bot
— `{PREFIX}crimes`: show all of my crimes
— `{PREFIX}nut`: sacrifice NUT to me''', # praise f strings 2: electric boogaloo
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text=f'that\'s all for now, go suggest stuff using {PREFIX}feedback if you want me to add stuff ig',
                        icon_url=EMBED_ICON
                    )
                    .set_thumbnail (
                        url=BIG_GIF
                    ),
                    view=Delete_Button(),
                    mention_author=False
                )


            # every command that requires arguments goes here


            elif len(WORD_LIST) >= 1: # deletes original message and sends the sentence back
                if COMMAND == 'say':
                    await message.delete ()
                    await message.channel.send (SENTENCE)

                elif COMMAND == 'wikipedia':
                    try:
                        await message.reply ( # this atrocity takes the input, finds a wikipedia article, and trims it to 1900 characters
                            f'```{wikipedia.page(SENTENCE).content[0:1900]}```',
                            view=Delete_Button(),
                            mention_author=False
                        )

                    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError): # if there's no article with that name catches error and gives info
                        await message.reply (
                            embed = discord.Embed (
                                title = 'insert helpful error name here',
                                description='multiple/no wikipedia article found with that name',
                                color = EMBED_COLOR
                            )
                            .set_footer (
                                text='you\'re still an absolute clampongus though',
                                icon_url=EMBED_ICON
                            ),
                            view=Delete_Button(),
                            mention_author=False
                        )

                elif COMMAND == '8ball' or COMMAND == 'ball':
                    await message.reply (
                        embed = discord.Embed (
                            title=SENTENCE,
                            description=random.choice ([ # you can add as many options as you want to this list
                                'yes', 
                                'no', 
                                'maybe', 
                                'idk', 
                                'ask later', 
                                'definitely', 
                                'never', 
                                'never ask me that again'
                            ]),
                            color=EMBED_COLOR
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )

                elif COMMAND == 'suggest' or COMMAND == 'feedback':
                    await SUGGEST_CHANNEL.send ( # sends to hardcoded suggestion channel
                        embed = discord.Embed (
                            title = f'feedback sent by **{message.author}**:',
                            description = f'sent in {message.channel.mention}: ```{SENTENCE}```',
                            color = EMBED_COLOR
                        )
                        .set_footer (
                            text='idk maybe react to this if you complete it or something',
                            icon_url=EMBED_ICON
                        )
                    )

                    await message.reply ( # sends confirmation message to user
                        embed = discord.Embed (
                            title = f'your feedback has been sent to {DEVELOPER}:',
                            description = f'```{SENTENCE}```',
                            color = EMBED_COLOR
                        )
                        .set_footer (
                            text='in the meantime idk go touch grass',
                            icon_url=EMBED_ICON
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )
                
                elif COMMAND == 'prefix' or COMMAND == 'setprefix':
                    if WORD_LIST[0] == 'reset':
                        try:
                            del DATABASE[f'prefix_{message.guild.id}'] # removes value entirely
                            await write_database() # wries the DATABASE dictionbary into the actual json file
                            await message.reply (
                                embed = discord.Embed (
                                    title='server prefix has been reset',
                                    description=f'you can set it again using `{PREFIX}prefix <prefix>`',
                                    color=EMBED_COLOR
                                ),
                                view=Delete_Button(),
                                mention_author=False
                            )
                        except KeyError:
                            await message.reply (
                                embed = discord.Embed (
                                    title='insert helpful error name here',
                                    description = 'there was no prefix set for this server',
                                    color=EMBED_COLOR
                                )
                                .set_footer (
                                text='you\'re still an absolute clampongus though',
                                icon_url=EMBED_ICON
                                ),
                                view=Delete_Button(),
                                mention_author=False
                            )
                    else:
                        DATABASE[f'prefix_{message.guild.id}'] = f'{SENTENCE[0]}' # writes the prefix to the DATABASE dictionary variable
                        await write_database() # writes the DATABASE dictionary into the database.json file
                        await message.reply (
                            embed = discord.Embed (
                                title=f'server prefix changed to {WORD_LIST[0]}',
                                description=f'you can change it back using `{PREFIX}prefix reset`',
                                color=EMBED_COLOR
                            ),
                            view=Delete_Button(),
                            mention_author=False
                        )
                
                elif COMMAND == 'len' or COMMAND == 'length': # this is a super simple command but tbh it's pretty useful
                    await message.reply (
                        embed = discord.Embed (
                            title=f'Your sentence is {len(SENTENCE)} characters long and {len(WORD_LIST)} words long:',
                            description = f'```{SENTENCE}```',
                            color=EMBED_COLOR
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )

                else:
                    await message.reply ( # generic error handling
                        embed = discord.Embed (
                            title='insert helpful error name here',
                            description='too lazy to implement proper errors but you probably sent too much stuff, not enough stuff, or something that\'s not a command',
                            color=EMBED_COLOR
                        )
                        .set_footer (
                            text='you\'re still an absolute clampongus though',
                            icon_url = EMBED_ICON
                        ),
                        view=Delete_Button(),
                        mention_author=False
                    )

            else:
                await message.reply ( # generic error handling 2
                    embed = discord.Embed (
                        title='insert helpful error name here',
                        description='too lazy to implement proper errors but you probably sent too much stuff, not enough stuff, or something that\'s not a command',
                        color=EMBED_COLOR
                    )
                    .set_footer (
                        text='you\'re still an absolute clampongus though',
                        icon_url = EMBED_ICON
                    ),
                    view=Delete_Button(),
                    mention_author=False
                )

intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
client = Main(intents=intents)

client.run (TOKEN)