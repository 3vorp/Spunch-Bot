import discord, os, wikipedia, random, json, datetime, dotenv
from discord.ext import commands
from config import * # saves me from having to use config.VARIABLE for everything
from help_strings import * # same thing

intents = discord.Intents.default()
intents.message_content = True # special permission required for messages
bot = commands.Bot(intents = intents, command_prefix = DEFAULT_PREFIX) # creating the actual bot client
bot.remove_command('help')

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
    global deletable
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



@bot.command()
async def nut(ctx, *, SENTENCE):
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

dotenv.load_dotenv() # stops token from being in public files
bot.run(os.getenv('TOKEN')) # the actual execution command