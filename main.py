import discord, os, wikipedia, random, json, datetime, dotenv, help_strings, config
from discord.ext import commands

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
    print('\033[91m\033[1mERROR: check the README.md more closely:\n\nTL;DR: create a database.json file inside the root folder following the formatting of the database_example.json example file\n\nThe bot will mostly work without a database, however commands such as prefix and nut will not.') # that weird stuff at the beginning handles the color

DEVELOPER = config.DEVELOPER
EMBED_COLOR = config.EMBED_COLOR
EMBED_ICON = config.EMBED_ICON
BIG_ICON = config.BIG_ICON
EMBED_GIF = config.EMBED_GIF
BIG_GIF = config.BIG_GIF

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
bot = commands.Bot(command_prefix = config.DEFAULT_PREFIX, intents = intents)
bot.remove_command("help")

async def write_database(): # I'd be copy and pasting this constantly so this saves me a LOT of time
    with open (os.path.join(os.path.dirname (__file__), 'database.json'), 'w', encoding = 'utf-8') as db: # same thing as reading from the DB
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
    async def button_clicked(self, interaction:discord.Interaction, button:discord.ui.Button): # whenever button is clicked calls this function
        await interaction.message.delete()



class Main(discord.Client):
    async def on_ready(self): # starts the bot
        STARTUP_CHANNEL = bot.get_channel(1034609478005436436) # hardcoded channel ids for a private server, change these if you fork this
        await STARTUP_CHANNEL.send (
            embed = discord.Embed (
                title = f'hello i\'m alive now',
                description = f'```started at {" ".join(datetime.datetime.now().strftime("%c").split())}```', # the redundant .join() and .split() methods removes a really annoying double space
                color = EMBED_COLOR
            )
            .set_footer (
                text = f'Online as {bot.user}',
                icon_url = EMBED_ICON
            )
        )
        await bot.change_presence(activity = discord.Game('spongeboy gif on repeat')) # discord activity

    async def on_message(self, message):
        if message.author == bot.user or message.content == '': # makes sure the bot can't reply to itself and cause an infinite loop
            return

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
            ) # thanks complibot (https://github.com/Faithful-Resource-Pack/Discord-Bot)
        
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
        
        if 'nut' == SENTENCE:
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
try:
    @bot.command()
    async def help(ctx):
        await ctx.reply("test")
except (discord.ext.command.errors.CommandNotFound):
    @bot.event()
    async def error(payload):
        await payload.reply("no command exists")

bot.run(TOKEN)