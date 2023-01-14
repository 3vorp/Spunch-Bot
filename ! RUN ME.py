import discord, os, wikipedia, random, json, time, dotenv, info_strings
from discord.ext import commands
from config import * # saves me from having to use config.VARIABLE for everything



### BOT / PREFIX SETUP ###



async def get_prefix(_, message): # somehow this actually works exactly how the old setup did
    global PREFIX # only needs to be declared global once since value is constant

    try: # assigns server prefix if one exists, if not use default prefix
        PREFIX = DATABASE[f'prefix_{message.guild.id}']

    except KeyError:
        PREFIX = DEFAULT_PREFIX

    return PREFIX

bot = commands.Bot ( # generating the actual bot client
    intents = discord.Intents.all(), # permission stuff
    command_prefix = get_prefix, # idk how this doesn't need parentheses but it works
    case_insensitive = True, # this and prefix spaces are for mobile users mostly
    strip_after_prefix = True # I hate when bots don't do this
)
bot.remove_command('help') # default help command is garbage and idk why it's there honestly



### DATABASE ###



try:
    with open('database.json', 'r') as db:
        DATABASE = json.load(db)

except FileNotFoundError:
    print(info_strings.error_database) # no eval() necessary because it's not an f string
    DATABASE = {} # stops initial errors, still won't really work though

async def write_database(): # saves a LOT of copy paste
    with open('database.json', 'w') as db:
        json.dump(DATABASE, db, indent = 4, ensure_ascii = False)



### STARTUP MESSAGE / PRESENCE ###



@bot.event
async def on_ready():
    global deletable
    await bot.change_presence (
        activity = discord.Game ( # shows "playing spongeboy gif on repeat"
            name = 'spongeboy gif on repeat'
        )
    )

    deletable = False
    await bot.get_channel(STARTUP_CHANNEL).send (
        embed = discord.Embed ( # time.time() is a unix timestamp
            title = 'hello i\'m alive now',
            description = f'''started at <t:{int(time.time())}>''',
            color = EMBED_COLOR
        )
        .set_footer (
            text = f'Online as {bot.user}',
            icon_url = EMBED_GIF
        )
    )



### DELETE BUTTON / REACTION ###



deletable = True # global variable for whether to add delete reaction or not

@bot.event
async def on_raw_reaction_add(payload): # raw events can handle all messages and not just cache
    global deletable
    if isinstance(payload.channel_id, discord.channel.DMChannel):
        return # ignore dms
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji = payload.emoji.name)
    user = payload.member # basically just boilerplate, tradeoff for working with raw events lol

    try:
        user_list = [i async for i in reaction.users()] # generates list of people who reacted

    except AttributeError: # sometimes reaction.users() stops existing and idk why but this fixes it
        pass

    if bot.user not in user_list or user == bot.user:
        return # additional guard clauses to prevent abuse/errors



    if reaction.emoji == '🗑️' and message.author == bot.user:
        try: # tries locating the original message for checking permissions
            original = await bot.get_channel(message.reference.channel_id).fetch_message(message.reference.message_id)
            if original.author != user: # checks if the original command is the same as the reactor

                deletable = False
                await user.send (
                    embed = discord.Embed (
                        title = 'you can\'t do that',
                        description = 'only the original sender can delete bot messages',
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = 'if you\'re moderating just use the delete button lol',
                        icon_url = EMBED_GIF
                    )
                )
                return

        except AttributeError: # passes to delete the message if there's no reply
            pass

        await message.delete() # if there's no reply and the original author is the reactor the message is deleted



### GLOBAL ANNOUNCEMENTS ###



    if reaction.emoji == '✅' and message.channel.id == ANNOUNCEMENT_CHANNEL:
        if '\n' in message.content:
            announcement_list = message.content.split('\n', 1)
        else: # if no title is provided just use "global announcement" as title
            announcement_list = ['GLOBAL ANNOUNCEMENT', message.content]

        for guild in bot.guilds: # just sends in the first channel available lol

            deletable = False
            await guild.text_channels[0].send (
                embed = discord.Embed (
                    title = announcement_list[0],
                    description = announcement_list[1],
                    color = EMBED_COLOR
                )
            )

        await message.clear_reactions() # stops accidental double reactions or cannodling etc


    if reaction.emoji == '❌' and message.channel.id == ANNOUNCEMENT_CHANNEL:
        await message.clear_reactions() # prevents people from being able to send it, effectively cancels


@bot.event
async def on_message(message):
    global deletable
    if deletable and message.author == bot.user: # automatically applies by default
        await message.add_reaction('🗑️')
        return # nothing else uses bot messages so this stops infinite loops

    else: # resets the status for the next message
        deletable = True



    if message.channel.id == ANNOUNCEMENT_CHANNEL: # initializes global announcements
        await message.add_reaction('✅') # the rest of the code is handled in on_raw_reaction_add()
        await message.add_reaction('❌')



### GENERAL / JOKE RESPONSES ###



    sentence = message.content.lower() # removes case sensitivity

    match sentence: # only direct matches go here
        case 'f':
            await message.add_reaction('🇫')

        case 'monke':
            await message.add_reaction('🎷')
            await message.add_reaction('🐒')

        case 'baller':
            await message.reply (
                'https://bit.ly/3UY1D0M', # original url was like 130 characters
                mention_author = False
            )

        case 'spongeboy':
            await message.reply (
                embed = discord.Embed (
                    color = EMBED_COLOR
                )
                .set_image (
                    url = BIG_GIF
                ),
                mention_author = False
            )

        case 'vine boom':
            await message.reply (
                'https://bit.ly/3XgGYGJ',
                mention_author = False
            )

        case 'hello there':
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

        case _ if 'forgor' in sentence: # this was a pain to implement but at least it's consistent
            await message.add_reaction('💀')

        case _ if 'bogos binted' in sentence: # allows for more variation
            await message.add_reaction('👽')

        case _ if 'mhhh' in sentence: # "mhhh moment" will still count, etc
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

        case _:
            await bot.process_commands(message) # allows commands to actually run



### ERROR HANDLING ###



@bot.event
async def on_command_error(ctx, error):
    await ctx.reply ( # handles basically all errors
        embed = discord.Embed (
            title = 'insert helpful error name here',
            description = f'```{error}```\n**use `{PREFIX}help` for a list of commands**',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'you\'re still an absolute clampongus though',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )



### UTILITY COMMANDS ###



@bot.command(aliases = ['wiki', 'w'])
async def WIKIPEDIA(ctx, *, search): # "*" puts message into next variable as-is
    try:
        article = wikipedia.page(search, pageid = None, auto_suggest = False)
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
                description = f'no wikipedia article called "{search}" was found',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'you\'re still an absolute clampongus though',
                icon_url = EMBED_GIF
            ),
            mention_author = False
        )

    except wikipedia.exceptions.DisambiguationError as error:
        final = ', '.join(f'{i}' for i in error.options[:-1]).lower()
        final += f', and {error.options[-1].lower()}' # yes I wanted it to be formatted nicely

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

@bot.command(aliases = ['suggest', 'f'])
async def FEEDBACK(ctx, *, message):
    global deletable # modifying value so every function that uses it declares it global

    deletable = False
    await bot.get_channel(SUGGEST_CHANNEL).send ( # edit this channel in config.py
        embed = discord.Embed (
            title = f'feedback sent by **{ctx.author}**:',
            description = f'sent in {ctx.channel.mention}: ```{message}```',
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
            description = f'```{message}```',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'in the meantime idk go touch grass',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )

@bot.command(aliases = ['prefix', 'p'])
async def SETPREFIX(ctx, *, new_prefix):
    if new_prefix == 'reset' or DEFAULT_PREFIX == new_prefix:
        try:
            del DATABASE[f'prefix_{ctx.guild.id}'] # removes value entirely
            await write_database() # writes DATABASE dictionary into the json
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
        return # fancy guard clause, saves indentation so I use these everywhere

    DATABASE[f'prefix_{ctx.guild.id}'] = f'{new_prefix}' # convenient to use guild id as key
    await write_database() # writes the DATABASE dictionary into the database.json file

    await ctx.reply (
        embed = discord.Embed (
            title = f'server prefix changed to {new_prefix}',
            description = f'you can change it back using `{new_prefix}prefix reset`',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'this was painful to implement so you better appreciate it',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )

@bot.command(aliases = ['len', 'l'])
async def LENGTH(ctx, *, sentence):
    word_list = sentence.split() # you need both word list and sentence

    if len(sentence) == 1: # grammar stuff because I'm a perfectionist lol
        character = 'character'
    else:
        character = 'characters'

    if len(word_list) == 1:
        word = 'word'
    else:
        word = 'words'

    await ctx.reply (
        embed = discord.Embed (
            title = f'your sentence is {len(sentence)} {character} long and {len(word_list)} {word} long:',
            description = f'```{sentence}```',
            color = EMBED_COLOR
        ),
        mention_author = False
    )

@bot.command(aliases = ['git', 'g'])
async def GITHUB(ctx):
    await ctx.reply (
        embed = discord.Embed (
            title = 'you can find my code on github here:',
            description = 'https://github.com/3vorp/Spunch-Bot',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'fair warning that it\'s kinda a dumpster fire to read through',
            icon_url = EMBED_GIF
        )
        .set_thumbnail (
            url = 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'
        ),
        mention_author = False
    )

@bot.command(aliases = ['h', 'info', 'i'])
async def HELP(ctx, search = 'all'): # only really need to track the first word
    if search == 'all':
        await ctx.reply (
            embed = discord.Embed ( # passed variables need to be evaluated per-message
                title = '**spunch bot**',
                description = eval(f'f"""{info_strings.help_all}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = eval(f'f"""{info_strings.help_footer}"""'),
                icon_url = EMBED_GIF
            )
            .set_thumbnail (
                url = BIG_GIF
            ),
            mention_author = False
        )
        return

    for i in info_strings.help_list: # iterates through the main command list
        if search in i[0]: # i[0] is always a tuple of the command aliases for any given command
            command = ', '.join(f'{PREFIX}{j}' for j in i[0]) # list comprehension to string
            await ctx.reply (
                embed = discord.Embed ( # same reason for using eval() as in the main help command
                    title = eval(f'f"""help for {command}"""'), # formatted list of aliases
                    description = eval(f'f"""{i[1]}"""'), # grabs description from second index
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = eval(f'f"""{info_strings.help_footer}"""'),
                    icon_url = EMBED_GIF
                )
                .set_thumbnail (
                    url = BIG_GIF
                ),
                mention_author = False
            )
            return # only needs to check for one match, otherwise it's just wasting resources

    await ctx.reply ( # if the return statement was never reached it probably doesn't exist
        embed = discord.Embed (
            title = 'insert helpful error name here',
            description = eval(f'f"""{info_strings.help_not_found}"""'),
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'you\'re still an absolute clampongus though',
            icon_url = EMBED_GIF
        ),
        mention_author = False
    )



### FUN COMMANDS ###



@bot.command(aliases = ['s'])
async def SAY(ctx, *, sentence):
    global deletable
    await ctx.message.delete()

    deletable = False # having a delete button next to bot text looked weird
    await ctx.channel.send(sentence)

@bot.command(aliases = ['e'])
async def EMBED(ctx, *, args): # can't split by spaces so needs to be passed in one string
    global deletable # this command is useful for server info so it's not deletable
    arg_list = args.split(';') # so you can have spaces in the embed

    if arg_list[0].startswith('https://') or arg_list[0].startswith('http://'):
        IMAGE = arg_list[0] # this way you can have image embeds and titles
        TITLE = None
    else:
        TITLE = arg_list[0]
        IMAGE = None

    try: # just sets it to nothing/defaults if nothing is specified
        DESCRIPTION = arg_list[1]
    except IndexError: # passes into except clause if any argument isn't provided
        DESCRIPTION = ''

    try:
        COLOR = arg_list[2].strip().lstrip('#') # discord.py is VERY picky with hex
        if COLOR: # if not empty
            COLOR = int(COLOR, base = 16) # converts into hex number/base 16
        else: # trigger the except if no color is provided
            raise IndexError
    except (IndexError, ValueError): # also catches invalid colors
        COLOR = EMBED_COLOR

    try:
        FOOTER = arg_list[3]
    except IndexError:
        FOOTER = ''

    try:
        FOOTER_IMAGE = arg_list[4]
    except IndexError:
        FOOTER_IMAGE = None

    try:
        THUMBNAIL = arg_list[5]
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

@bot.command(aliases = ['8ball', 'b'])
async def BALL(ctx, *, question = ''): # you can ask for opinion without input
    ball_choices = [ # infinitely expandable list
        'yes', 'no',
        'maybe', 'idk',
        'ask later', 'definitely',
        'never', 'never ask me that again',
        'yesn\'t', 'doubt'
    ]

    if question: # checks if exists
        description = f'```{question}```'
    else: # sets blank if it doesn't exist
        description = ''

    await ctx.reply ( # if no option provided no description will be set
        embed = discord.Embed (
            title = random.choice(ball_choices),
            description = description,
            color = EMBED_COLOR
        ),
        mention_author = False
    )

@bot.command(aliases = ['roll', 'd', 'r'])
async def DICE(ctx, count: int = 1, sides: int = 6): # needs to be int for number stuff
    rolls = [random.randint(1, sides) for _ in range(count)] # _ ignores iterator

    if count > 1: # won't show roll count if there was only one roll and no need for a sum
        footer = f'if you\'re interested these were the results for each roll: {rolls}'
        icon_url = EMBED_GIF
    else:
        footer = ''
        icon_url = None

    await ctx.reply (
        embed = discord.Embed (
            title = f'you rolled **{sum(rolls)}**',
            description = f'using {count} {sides}-sided dice',
            color = EMBED_COLOR
        )
        .set_footer (
            text = footer,
            icon_url = icon_url
        ),
        mention_author = False
    )

@bot.command(aliases = ['m'])
async def MOCK(ctx, *, sentence):
    mocked_word = list(sentence.lower()) # list of characters rather than words
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

@bot.command(aliases = ['u', 'owo']) # I'm so sorry
async def UWU(ctx, *, sentence):
    char_list = list(sentence.lower())
    uwu_word = ''
    for i in range(len(char_list)):
        try:
            char_list[i+1] # there's no next index if it's on the final character
        except IndexError:
            char_list.append('') # just adds an empty string to stop final errors

        match char_list[i]: # much easier to read than a ton of elif statements
            case 'l' | 'r':
                uwu_word += 'w'

            case 'o' | 'a' | 'u' | 'i' | 'e': # can be reused for multiple vowels
                if char_list[i-1] == 'n' or char_list[i-1] == 'm':
                    uwu_word += f'y{char_list[i]}' # adds y for maximum uwu

                elif (char_list[i-1] == ' ' and char_list[i+1] != ' ') or i-1 <= 0:
                    if random.randint(0, 4) == 0: # stutter only happens occasionally
                        uwu_word += f'{char_list[i]}-{char_list[i]}'

                    else:
                        uwu_word += char_list[i]

                else:
                    uwu_word += char_list[i]

            case 't':
                if char_list[i+1] == 'h':
                    uwu_word += 'd' # replaces th with d
                    char_list.pop(i+1) # gets rid of the next entry to stop the h from coming back

                else:
                    uwu_word += 't'

            case '.':
                uwu_word += '~'

            case '!':
                chance = random.randint(0, 5)
                if chance == 0:
                    uwu_word += '!!!'
                if chance == 1:
                    uwu_word += '!♡♡♡'
                if chance == 2:
                    uwu_word += '!! ^w^'
                else: # there's a 50% chance that nothing happens to stop things getting too crazy
                    uwu_word += char_list[i]

            case '?':
                chance = random.randint(0, 5)
                if chance == 0:
                    uwu_word += '?~'
                if chance == 1:
                    uwu_word += '?~ >w<'
                if chance == 2:
                    uwu_word += '? ✧﹡:･ﾟ✧'
                else: # same goes here
                    uwu_word += char_list[i]

            case _: # if no key letters are triggered it just adds the letter as-is
                uwu_word += char_list[i]

    await ctx.reply (
        embed = discord.Embed (
            title = 'i hate this as much as you do',
            description = f'```{uwu_word}```',
            color = EMBED_COLOR
        ),
        mention_author = False
    )


@bot.command(aliases = ['rps'])
async def ROCKPAPERSCISSORS(ctx, user_answer = random.choice(['rock', 'paper', 'scissors'])):
    bot_answer = random.choice(['rock', 'paper', 'scissors'])

    if bot_answer == user_answer:
        await ctx.reply (
            embed = discord.Embed (
                title = 'it\'s a tie',
                description = f'you sent {user_answer}, i sent {bot_answer}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    elif ( # pain
        (user_answer == 'scissors' and bot_answer == 'paper') or
        (user_answer == 'paper' and bot_answer == 'rock') or
        (user_answer == 'rock' and bot_answer == 'scissors')
    ):
        await ctx.reply (
            embed = discord.Embed (
                title = 'you win',
                description = f'you sent {user_answer}, i sent {bot_answer}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    elif ( # pain II
        (user_answer == 'paper' and bot_answer == 'scissors') or
        (user_answer == 'rock' and bot_answer == 'paper') or
        (user_answer == 'scissors' and bot_answer == 'rock')
    ):
        await ctx.reply (
            embed = discord.Embed (
                title = 'i win',
                description = f'you sent {user_answer}, i sent {bot_answer}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    else:
        await ctx.reply (
            embed = discord.Embed (
                title = 'that wasn\'t an option so i automatically win :sunglasses:',
                description = f'you sent {user_answer}, i sent {bot_answer}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

@bot.command(aliases = ['n'])
async def NUT(ctx, *, query = None):
    if query == 'total' or query == 'amount':
        await ctx.reply (
            embed = discord.Embed (
                title = f'total amount of NUT: **{DATABASE["nut_count"]}**',
                description = 'all fine additions to my collection',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return

    DATABASE['nut_count'] = DATABASE['nut_count'] + 1
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

dotenv.load_dotenv() # keeps token out of public files
bot.run(os.getenv('TOKEN')) # the actual execution command