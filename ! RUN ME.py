import discord, os, wikipedia, random, json, time, dotenv, info_strings
from discord.ext import commands
from config import * # saves me from having to use config.VARIABLE for everything



### BOT / PREFIX SETUP ###



async def get_prefix(_, message): # somehow this actually works exactly how the old setup did
    global PREFIX # only needs to be declared global once since value is constant

    try: # assigns server prefix if one exists, if there's errors it just sets to the default
        PREFIX = DATABASE[f'prefix_{message.guild.id}']

    except (KeyError, AttributeError): # AttributeError from DMs, KeyError from no server prefix
        PREFIX = DEFAULT_PREFIX

    return PREFIX

bot = commands.Bot ( # generating the actual bot client
    intents = discord.Intents.all(), # permission stuff
    command_prefix = get_prefix, # apparently you can pass functions as arguments
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



### RANDOM UTILITIES ###



async def get_reply_content(ctx): # I'm not touching this ever again the function name is self-explanatory
    if len(ctx.message.content.split()) > 1:
        return None # if there's already message content no need to look for replies

    elif ctx.message.reference:
        original = (await bot # fetches original message if it exists
            .get_channel(ctx.message.reference.channel_id)
            .fetch_message(ctx.message.reference.message_id)
        )
        original_ctx = await bot.get_context(original)

        if original_ctx.message.content: # tries to find message content in the original message
            return original_ctx.message.content

        elif original_ctx.message.embeds: # if all else fails search for embeds (if replying to bot etc)
            if original_ctx.message.embeds[0].title:
                return original_ctx.message.embeds[0].title
            elif original_ctx.message.embeds[0].description: # only uses description if no title set
                return original_ctx.message.embeds[0].description

    return None # if there's no message reference and no message content/embeds then there's nothing to get



### STARTUP MESSAGE / PRESENCE ###



@bot.event
async def on_ready():
    global deletable
    await bot.tree.sync()
    await bot.change_presence (
        activity = discord.Game ( # shows "playing spunch bop gif"
            name = 'spunch 🅱op gif'
        )
    )

    last_start = [ # used to check whether to reset the wordle
        message async for message in (bot
            .get_channel(STARTUP_CHANNEL)
            .history(limit = 1)
        )
    ]

    deletable = False
    new_start = await bot.get_channel(STARTUP_CHANNEL).send (
        embed = discord.Embed ( # time.time() is a unix timestamp
            title = 'hello i\'m alive now',
            description = f'started at <t:{int(time.time())}>',
            color = EMBED_COLOR
        )
        .set_footer (
            text = f'online as {bot.user}',
            icon_url = ICON_URL
        )
    )

    if last_start[0].created_at.date() != new_start.created_at.date():
        with open('assets/wordle_answers.txt', 'r') as f: # generates new wordle if it's a new day
            DATABASE['wordle'] = random.choice(f.read().split('\n'))
            await write_database()



### REACTION BOILERPLATE ###



deletable = True # global variable for whether to add delete reaction or not

@bot.event
async def on_raw_reaction_add(payload): # raw events can handle all messages and not just cache
    global deletable
    try: # in DMs some of these break so this just silences that
        message = (await bot
            .get_channel(payload.channel_id)
            .fetch_message(payload.message_id)
        )

        reaction = discord.utils.get (
            message.reactions,
            emoji = payload.emoji.name
        )

        user = payload.member
        user_list = [i async for i in reaction.users()] # generates list of people who reacted

    except AttributeError: # sometimes reaction.users() stops existing also so yeah
        return # ignores action if anything goes wrong since yeah

    if bot.user not in user_list or bot.user == user:
        return # additional guard clauses to prevent abuse/errors



### DELETE REACTION ###



    if reaction.emoji == '🗑️' and message.author == bot.user:
        try: # checks permissions by looking at original message author and user permissions
            original = (await bot
                .get_channel(message.reference.channel_id)
                .fetch_message(message.reference.message_id)
            )

            if original.author != user and not user.guild_permissions.manage_messages:
                deletable = False # if the user has mod perms they can delete using the reaction
                await user.send ( # sends in DMs to not clutter chats further
                    embed = discord.Embed (
                        title = 'you can\'t do that',
                        description = 'only the original sender can delete bot messages',
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = 'also if you have manage message perms yeah that works too',
                        icon_url = ICON_URL
                    )
                )
                return

        except (AttributeError, discord.errors.NotFound): # if no reply/slash command
            pass

        await message.delete() # only happens if all these checks pass



### FEEDBACK HANDLER



    elif message.channel.id == SUGGEST_CHANNEL and user.id in DEVELOPER_IDS:
        fetchable = True
        try:
            link = [int(i) for i in message.embeds[0].url.split('/')[-2:]]

            fetched_message = (await bot # parsing url into more readable format
                .get_channel(link[0])
                .fetch_message(link[1])
            ) # fetching message using the parsed url

        except (AttributeError, discord.errors.NotFound):
            fetchable = False # checks whether to update the original message or not

        if reaction.emoji == '✅':
            await message.edit (
                embed = discord.Embed (
                    title = message.embeds[0].title,
                    url = message.embeds[0].url,
                    description = message.embeds[0].description,
                    color = GREEN_COLOR
                )
                .set_footer (
                    text = 'suggestion has been implemented',
                    icon_url = ICON_URL
                )
            )

            if fetchable: # only edits original confirmation if it exists to prevent errors
                await fetched_message.edit (
                    embed = discord.Embed (
                        title = fetched_message.embeds[0].title,
                        description = fetched_message.embeds[0].description,
                        color = GREEN_COLOR
                    )
                    .set_footer (
                        text = 'suggestion has been implemented, look out for the next changelog',
                        icon_url = ICON_URL
                    )
                )

            await message.clear_reactions() # remove reactions from original message

        elif reaction.emoji == '❌':
            await message.edit (
                embed = discord.Embed (
                    title = message.embeds[0].title,
                    url = message.embeds[0].url,
                    description = message.embeds[0].description,
                    color = RED_COLOR
                )
                .set_footer (
                    text = 'suggestion will not be implemented',
                    icon_url = ICON_URL
                )
            )

            if fetchable:
                await fetched_message.edit (
                    embed = discord.Embed (
                        title = fetched_message.embeds[0].title,
                        description = fetched_message.embeds[0].description,
                        color = RED_COLOR
                    )
                    .set_footer (
                        text = 'suggestion will not be implemented',
                        icon_url = ICON_URL
                    )
                )

            await message.clear_reactions()



### GLOBAL ANNOUNCEMENTS ###



    elif reaction.emoji == '✅' and message.channel.id == ANNOUNCEMENT_CHANNEL and user.id in DEVELOPER_IDS:
        if '\n' in message.content:
            announcement_list = message.content.split('\n', 1)
        else: # if no title is provided just use "global announcement" as title
            announcement_list = ['GLOBAL ANNOUNCEMENT', message.content]

        for guild in bot.guilds: # sends to each server
            try: # tries to get a custom announcement channel
                channel = bot.get_channel(DATABASE[f'announcement_{guild.id}'])
            except KeyError: # if none exists set it to the first available
                channel = guild.text_channels[0]

            if channel: # ignores server if it's turned off

                deletable = False
                await channel.send (
                    embed = discord.Embed (
                        title = announcement_list[0],
                        description = announcement_list[1],
                        color = EMBED_COLOR
                    )
                    .set_footer (
                        text = f'you can use {PREFIX}setannouncements to set a custom announcement channel',
                        icon_url = ICON_URL
                    )
                )

        await message.clear_reactions() # stops accidental double reactions or canoodling etc

    if reaction.emoji == '❌' and message.channel.id == ANNOUNCEMENT_CHANNEL and user.id in DEVELOPER_IDS:
        await message.clear_reactions() # didn't want to delete message so copy/paste still works



@bot.event
async def on_message(message):
    global deletable
    if message.author == bot.user: # stops the bot replying to itself
        if deletable and not isinstance(message.channel, discord.channel.DMChannel):
            await message.add_reaction('🗑️') # DMs break with reactions badly

        return # nothing else uses bot messages so just stop early

    deletable = True # resets the status for the next message
    PREFIX = await get_prefix(None, message)
    ctx = await bot.get_context(message) # til you can just... create the ctx variable
    sentence = message.content.lower() # removes case sensitivity

    if message.channel.id == SUGGEST_CHANNEL: # automatically converts to suggestion format
        await FEEDBACK(ctx, message = sentence)
        await message.delete() # deletes original message to save hassle in feedback command


    if message.channel.id == ANNOUNCEMENT_CHANNEL: # initializes global announcements
        await message.add_reaction('✅') # actual pushing is in on_raw_reaction_add()
        await message.add_reaction('❌')



### KEYWORDS ###



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

        case 'spunch bop' | 'spongeboy':
            await message.reply (
                embed = discord.Embed (
                    color = EMBED_COLOR
                )
                .set_image (
                    url = THUMBNAIL_URL
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

    if sentence.startswith(bot.user.mention): # on bot mention without command listed
        await HELP(ctx) # passes the ctx created way above

    elif sentence.startswith('nut'):
        await NUT(ctx, query = sentence[4:]) # nut is both a keyword and a command because uhh yes

    elif 'forgor' in sentence: # I know this is ugly but at least it's consistent
        await message.add_reaction('💀')

    elif 'bogos binted' in sentence: # allows for more variation
        await message.add_reaction('👽')

    elif 'mhhh' in sentence: # "mhhh moment" will still count, etc
        await message.reply (
            embed = discord.Embed (
                title = 'mhhh',
                description = '```Uh-oh moment```',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'Swahili → English',
                icon_url = ICON_URL
            ),
            mention_author = False
        ) # thanks complibot (https://github.com/Faithful-Resource-Pack/Discord-Bot)

    elif sentence.startswith(PREFIX) and not sentence[len(PREFIX):].startswith(PREFIX):
        await bot.process_commands(message) # allows commands to actually run



### ERROR HANDLING ###



@bot.event
async def on_command_error(ctx, error):
    PREFIX = await get_prefix(None, ctx.message)
    print(error) # prints errors so you don't have to rely on the sent message
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply ( # for permission based commands
            embed = discord.Embed (
                title = 'you can\'t do that',
                description = f'```{error}```',
                color = RED_COLOR
            )
            .set_footer (
                text = 'instant ban',
                icon_url = ICON_URL
            ),
            mention_author = False
        )
        return

    await ctx.reply ( # handles basically all generic errors
        embed = discord.Embed (
            title = info_strings.error_title,
            description = f'```{error}```\n**use `{PREFIX}help` for a list of commands**',
            color = RED_COLOR
        )
        .set_footer (
            text = info_strings.error_clampongus,
            icon_url = ICON_URL
        ),
        mention_author = False
    )



### UTILITY COMMANDS ###



@bot.hybrid_command (
    name = 'wikipedia', # since it's a slash command prefix will always be slash
    description = info_strings.help_dict['wikipedia'],
    aliases = ['wiki', 'w']
)
@discord.app_commands.describe(search = 'your wikipedia search')
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
                title = info_strings.error_title,
                description = f'no wikipedia article called "{search}" was found',
                color = RED_COLOR
            )
            .set_footer (
                text = info_strings.error_clampongus,
                icon_url = ICON_URL
            ),
            mention_author = False
        )

    except wikipedia.exceptions.DisambiguationError as error:
        options = ', '.join(i for i in error.options[:-1]).lower()
        options += f', and {error.options[-1].lower()}' # yes I wanted it to be formatted nicely

        await ctx.reply (
            embed = discord.Embed (
                title = 'multiple options found:',
                description = f'{options} are all possible options',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'be more specific',
                icon_url = ICON_URL
            ),
            mention_author = False
        )

@bot.hybrid_command (
    name = 'feedback',
    description = info_strings.help_dict['feedback'],
    aliases = ['suggest', 'f']
)
@discord.app_commands.describe(message = 'the message you want to send; please be specific')
async def FEEDBACK(ctx, *, message):
    global deletable # modifying value so every function that uses it declares it global

    if ctx.channel.id != SUGGEST_CHANNEL: # only sends confirmation if it's not in the channel
        confirmation = await ctx.reply ( # assigned to variable so it can be linked to later
            embed = discord.Embed (
                title = 'your feedback has been sent:',
                description = f'```{message}```',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'this status will be changed when something has happened',
                icon_url = ICON_URL
            ),
            mention_author = False
        )
        url = confirmation.jump_url # previous message was assigned as a variable to do this

    else: # if it's in the feedback channel
        if ctx.interaction:
            msg = await ctx.send('** **') # completes interaction for slash command
            await msg.delete()

        url = None # if there's no reference url there's no point setting it

    deletable = False
    msg = await bot.get_channel(SUGGEST_CHANNEL).send ( # edit this channel in config.py
        embed = discord.Embed (
            title = f'feedback sent by **{ctx.author}**:',
            url = url,
            description = f'```{message}```',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'idk maybe react to this if you complete it or something',
            icon_url = ICON_URL
        )
    )

    await msg.add_reaction('✅') # actual pushing is in on_raw_reaction_add()
    await msg.add_reaction('❌')

@bot.hybrid_command (
    name = 'setprefix',
    description = info_strings.help_dict['setprefix'],
    aliases = ['prefix', 'p']
)
@discord.app_commands.describe (
    new_prefix = f'default is `{DEFAULT_PREFIX}`, use `reset` to reset prefix'
)
@commands.guild_only()
async def SETPREFIX(ctx, *, new_prefix):
    if new_prefix in ('reset', DEFAULT_PREFIX): # easier to check if in list than with `or`
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
                    title = info_strings.error_title,
                    description = 'there was no prefix set for this server',
                    color = RED_COLOR
                )
                .set_footer (
                    text = info_strings.error_clampongus,
                    icon_url = ICON_URL
                ),
                mention_author = False
            )
        return # fancy guard clause, saves indentation so I use these everywhere

    DATABASE[f'prefix_{ctx.guild.id}'] = new_prefix # convenient to use guild id as key
    await write_database() # writes the DATABASE dictionary into the database.json file

    await ctx.reply (
        embed = discord.Embed (
            title = f'server prefix changed to {new_prefix}',
            description = f'you can change it back using `{new_prefix}prefix reset`',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'this was painful to implement so you better appreciate it',
            icon_url = ICON_URL
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'setannouncements',
    description = info_strings.help_dict['setannouncements'],
    aliases = ['sa']
)
@discord.app_commands.describe (
    config = 'use `reset` to reset channel or `none` to disable for given server'
)
@commands.guild_only()
async def SETANNOUNCEMENTS(ctx, config = ''):
    if config == 'reset' or ctx.channel == ctx.guild.text_channels[0]:
        try:
            del DATABASE[f'announcement_{ctx.guild.id}']
            await write_database()
            await ctx.reply (
                embed = discord.Embed (
                    title = 'announcement channel has been reset',
                    description = f'default announcement channel is {ctx.guild.text_channels[0].mention}',
                    color = EMBED_COLOR
                ),
                mention_author = False
            )

        except KeyError:
            await ctx.reply (
                embed = discord.Embed (
                    title = info_strings.error_title,
                    description = 'there was no announcement channel set for this server',
                    color = RED_COLOR
                )
                .set_footer (
                    text = info_strings.error_clampongus,
                    icon_url = ICON_URL
                ),
                mention_author = False
            )
        return

    if config in ('off', 'none', 'false'):
        DATABASE[f'announcement_{ctx.guild.id}'] = False
        await write_database()
        await ctx.reply (
            embed = discord.Embed (
                title = 'announcements have been turned off for this server',
                description = f'you can still use `{PREFIX}changelog` to see the latest announcements',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return

    DATABASE[f'announcement_{ctx.guild.id}'] = ctx.channel.id
    await write_database()

    await ctx.reply (
        embed = discord.Embed (
            title = 'announcement channel set to this channel',
            description = f'you can change it back using `{PREFIX}setannouncements reset`',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'this command literally took me two months to implement kill me',
            icon_url = ICON_URL
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'changelog',
    description = info_strings.help_dict['changelog'],
    aliases = ['announcement']
)
@discord.app_commands.describe(amount = 'how many changelogs you want (defaults to one)')
async def CHANGELOG(ctx, amount: int = 1):
    changelogs = [ # scrapes the announcement channel for all recent messages
        message async for message in (bot
            .get_channel(ANNOUNCEMENT_CHANNEL)
            .history(limit = amount)
        )
    ] # why does this work but not the super obvious normal way

    for i in reversed(changelogs): # goes from oldest to newest to make sense
        if '\n' in i.content: # same code as in the actual announcement pusher
            announcement_list = i.content.split('\n', 1)
        else:
            announcement_list = ['GLOBAL ANNOUNCEMENT', i.content]

        await ctx.reply (
            embed = discord.Embed (
                title = announcement_list[0],
                description = announcement_list[1],
                timestamp = i.created_at,
                color = EMBED_COLOR
            )
            .set_footer ( # adds original send date just for fun
                text = 'originally sent at',
                icon_url = ICON_URL
            ),
            mention_author = False
        )

@bot.command(aliases = ['rm']) # yes this is a direct reference to the rm command in terminals
async def removemessage(ctx): # dev command for removing clutter the bot might have sent on accident
    if ctx.author.id not in DEVELOPER_IDS:
        await ctx.message.add_reaction('❌')
        return # returns early if you don't have permissions

    try:
        original = (await bot # directly copy/pasted from get_reply_content()
            .get_channel(ctx.message.reference.channel_id)
            .fetch_message(ctx.message.reference.message_id)
        )
        original_ctx = await bot.get_context(original)
        await original_ctx.message.delete()

    except AttributeError:
        pass

    await ctx.message.delete()

@bot.hybrid_command (
    name = 'length',
    description = info_strings.help_dict['length'],
    aliases = ['len', 'l']
)
@discord.app_commands.describe(sentence = 'pretty self explanatory lol')
async def LENGTH(ctx, *, sentence):
    word_list = sentence.split()

    character = 'character' if len(sentence) == 1 else 'characters'
    word = 'word' if len(word_list) == 1 else 'words' # proper plurals because I'm a perfectionlist lol

    await ctx.reply (
        embed = discord.Embed (
            title = f'your sentence is {len(sentence)} {character} long and {len(word_list)} {word} long:',
            description = f'```{sentence}```',
            color = EMBED_COLOR
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'license',
    description = info_strings.help_dict['license'],
    aliases = ['tos']
)
async def LICENSE(ctx):
    await ctx.reply (
        file = discord.File('license.txt'),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'github',
    description = info_strings.help_dict['github'],
    aliases = ['git', 'g']
)
async def GITHUB(ctx):
    await ctx.reply (
        embed = discord.Embed (
            title = 'you can find my code on github here:',
            description = 'https://github.com/3vorp/Spunch-Bot',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'fair warning that it\'s kinda a dumpster fire to read through',
            icon_url = ICON_URL
        )
        .set_thumbnail (
            url = 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'help',
    description = info_strings.help_dict['help'],
    aliases = ['h', 'info', 'i']
)
@discord.app_commands.describe(search = 'specific command to look for, or use `all` to show full list')
async def HELP(ctx, search = 'all'): # only really need to track the first word
    global PREFIX
    if ctx.interaction:
        PREFIX = '/'
    if search == 'all':
        await ctx.reply (
            embed = discord.Embed ( # passed variables need to be evaluated per-message
                title = '**spunch bot**',
                description = eval(f'f"""{info_strings.help_string}"""'),
                color = EMBED_COLOR
            )
            .set_footer (
                text = eval(f'f"""{info_strings.help_footer}"""'),
                icon_url = ICON_URL
            )
            .set_thumbnail (
                url = THUMBNAIL_URL
            ),
            mention_author = False
        )
        return

    for i in info_strings.help_list: # iterate through the main command list
        if search in i[0]: # i[0] is always a tuple of the command aliases for any given command
            command = ' / '.join(f'{PREFIX}{j}' for j in i[0]) # list comprehension to string
            await ctx.reply (
                embed = discord.Embed ( # same reason for using eval() as in the main help command
                    title = eval(f'f"""help for {command}"""'), # formatted list of aliases
                    description = eval(f'f"""{i[1]}\n{i[2]}"""'), # grabs description from second index
                    color = EMBED_COLOR
                )
                .set_footer (
                    text = eval(f'f"""{info_strings.help_footer}"""'),
                    icon_url = ICON_URL
                )
                .set_thumbnail (
                    url = THUMBNAIL_URL
                ),
                mention_author = False
            )
            return # only needs to check for one match, otherwise it's just wasting resources

    await ctx.reply ( # if the return statement was never reached it probably doesn't exist
        embed = discord.Embed (
            title = info_strings.error_title,
            description = eval(f'f"""{info_strings.help_not_found}"""'),
            color = RED_COLOR
        )
        .set_footer (
            text = info_strings.error_clampongus,
            icon_url = ICON_URL
        ),
        mention_author = False
    )



### FUN COMMANDS ###



@bot.hybrid_command (
    name = 'say',
    description = info_strings.help_dict['say'],
    aliases = ['s']
)
@discord.app_commands.describe(sentence = 'pretty self explanatory lol')
async def SAY(ctx, *, sentence):
    global deletable
    if ctx.interaction: # filter so that the slash command doesn't have the reply
        deletable = False
        msg = await ctx.send('** **')
        await msg.delete()
    else:
        await ctx.message.delete()

    deletable = False # having a delete button next to bot text looked weird
    await ctx.channel.send(sentence) # can't use ctx.send() because slash command

@bot.hybrid_command (
    name = 'embed',
    description = info_strings.help_dict['embed'],
    aliases = ['e']
)
@discord.app_commands.describe (
    title = 'title of embed',
    description = 'description of embed',
    color = 'color of embed in hex (e.g. #ff0000)',
    footer = 'footer text',
    footer_image = 'url to footer image/gif',
    thumbnail = 'url to thumbnail image/gif',
    image = 'url to full image'
)
async def EMBED (
    ctx, *,
    title = '',
    description = '',
    color = '',
    footer = '',
    footer_image = '',
    thumbnail = '',
    image = ''
):
    global deletable # this command is useful for server info so it's not deletable

    if ctx.interaction: # if slash command
        deletable = False
        msg = await ctx.send('** **') # needs to complete interaction to prevent error
        await msg.delete() # idk why you have to do it this way but oh well it works

        arg_list = [title, description, color, footer, footer_image, thumbnail, image]

    else: # if prefix command you can delete directly
        await ctx.message.delete()
        arg_list = title # in non-prefix commands everything gets passed into title
        arg_list = arg_list.split(';')

    if ''.join(arg_list) == '': # if nothing was sent
        await ctx.channel.send (
            embed = discord.Embed (
                title = info_strings.error_title,
                description = 'you need to actually provide arguments lol',
                color = RED_COLOR
            )
            .set_footer (
                text = info_strings.error_clampongus,
                icon_url = ICON_URL
            ),
            mention_author = False
        )
        return

    if image: # if the slash command passed a separate main image
        TITLE = arg_list[0]
        IMAGE = image
    else: # prefix command doesn't have thumbnail
        if arg_list[0].startswith('http'):
            TITLE = None
            IMAGE = arg_list[0]
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
        if arg_list[4].startswith('http'):
            FOOTER_IMAGE = arg_list[4]
        else:
            raise IndexError
    except IndexError:
        FOOTER_IMAGE = None

    try:
        if arg_list[5].startswith('http'):
            THUMBNAIL = arg_list[4]
        else:
            raise IndexError
    except IndexError:
        THUMBNAIL = None

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

@bot.hybrid_command (
    name = 'ball',
    description = info_strings.help_dict['ball'],
    aliases = ['8ball', 'b']
)
@discord.app_commands.describe(question = 'if left blank will just give answer')
async def BALL(ctx, *, question = ''): # you can ask for opinion without input
    description = question if question else await get_reply_content(ctx) # tries finding other options

    await ctx.reply (
        embed = discord.Embed (
            title = random.choice([ # infinitely expandable list
                'yes', 'no',
                'maybe', 'idk',
                'ask later', 'definitely',
                'never', 'never ask me that again',
                'yesn\'t', 'doubt'
            ]),
            description = f'```{description}```' if description else None,
            color = EMBED_COLOR
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'dice',
    description = info_strings.help_dict['dice'],
    aliases = ['roll', 'd', 'r']
)
@discord.app_commands.describe (
    count = 'number of dice (default 1)',
    sides = 'how many sides each dice has (default 6)'
)
async def DICE(ctx, count: int = 1, sides: int = 6): # needs to be int for number stuff
    rolls = [random.randint(1, sides) for _ in range(count)] # _ ignores iterator

    if count > 1 and len(rolls) <= 30: # won't show roll count if there was only one
        footer = f'individual rolls: {rolls}'
        icon_url = ICON_URL
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

@bot.hybrid_command (
    name = 'mock',
    description = info_strings.help_dict['mock'],
    aliases = ['m']
)
@discord.app_commands.describe(sentence = 'pretty self explanatory lol')
async def MOCK(ctx, *, sentence):
    mocked_word = [sentence.upper()[i] if i % 2 == 0 else sentence.lower()[i] for i in range(len(sentence))]

    await ctx.reply (
        embed = discord.Embed (
            title = 'imagine mocking other users over the internet couldn\'t be me',
            description = f'```{"".join(mocked_word)}```',
            color = EMBED_COLOR
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'uwu',
    description = info_strings.help_dict['uwu'],
    aliases = ['u', 'owo']
)
@discord.app_commands.describe(sentence = 'there\'s no going back')
async def UWU(ctx, *, sentence): # I'm so sorry
    char_list = list(sentence.lower())
    uwu_word = ''
    for i in range(len(char_list)):
        try:
            char_list[i+1] # there's no next index if it's on the final character
        except IndexError:
            char_list.append('') # just adds an empty string to stop final errors

        chance = random.randint(0, 5)
        match char_list[i]: # much easier to read than a ton of elif statements
            case 'l' | 'r':
                uwu_word += 'w'

            case 'o' | 'a' | 'u' | 'i' | 'e': # can be reused for multiple vowels
                if char_list[i-1] in ('n', 'm'):
                    uwu_word += f'y{char_list[i]}' # adds y for maximum uwu

                elif char_list[i-1] == ' ' and char_list[i+1] != ' ' and chance == 0:
                    uwu_word += f'{char_list[i]}-{char_list[i]}'

                else:
                    uwu_word += char_list[i]

            case 't':
                if char_list[i+1] == 'h':
                    uwu_word += 'd' # replaces th with d
                    char_list.pop(i+1) # stops the h from coming back by removing it

                else:
                    uwu_word += 't'

            case ',':
                match chance:
                    case 0:
                        uwu_word += ' 7w7,'
                    case 1:
                        uwu_word += ' •w•,'
                    case 2:
                        uwu_word += ' :3,'
                    case _:
                        uwu_word += char_list[i]

            case '.':
                match chance:
                    case 0:
                        uwu_word += ' uwu~'
                    case 1:
                        uwu_word += ' owo~'
                    case 2:
                        uwu_word += '☆..'
                    case _: # 50% chance of nothing happening, stops things from getting too chaotic
                        uwu_word += '~'

            case '!':
                match chance:
                    case 0:
                        uwu_word += '!!!'
                    case 1:
                        uwu_word += '!♡♡♡'
                    case 2:
                        uwu_word += '!! ^w^'
                    case _:
                        uwu_word += char_list[i]

            case '?':
                match chance:
                    case 0:
                        uwu_word += '?~'
                    case 1:
                        uwu_word += '?~ >w<'
                    case 2:
                        uwu_word += '? *:･ﾟ✧(ꈍᴗꈍ)✧･ﾟ:*'
                    case _:
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

@bot.hybrid_command (
    name = 'rockpaperscissors',
    description = info_strings.help_dict['rockpaperscissors'],
    aliases = ['rps']
)
@discord.app_commands.describe(choice = 'must be either `rock`, `paper`, or `scissors`')
async def ROCKPAPERSCISSORS(ctx, choice = random.choice (['rock', 'paper', 'scissors'])):
    bot_choice = random.choice(['rock', 'paper', 'scissors'])

    if bot_choice == choice:
        await ctx.reply (
            embed = discord.Embed (
                title = 'it\'s a tie',
                description = f'you sent {choice}, i sent {bot_choice}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    elif ( # pain
        (choice == 'scissors' and bot_choice == 'paper') or
        (choice == 'paper' and bot_choice == 'rock') or
        (choice == 'rock' and bot_choice == 'scissors')
    ):
        await ctx.reply (
            embed = discord.Embed (
                title = 'you win',
                description = f'you sent {choice}, i sent {bot_choice}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    elif ( # pain II
        (choice == 'paper' and bot_choice == 'scissors') or
        (choice == 'rock' and bot_choice == 'paper') or
        (choice == 'scissors' and bot_choice == 'rock')
    ):
        await ctx.reply (
            embed = discord.Embed (
                title = 'i win',
                description = f'you sent {choice}, i sent {bot_choice}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

    else:
        await ctx.reply (
            embed = discord.Embed (
                title = 'that wasn\'t an option so i automatically win :sunglasses:',
                description = f'you sent {choice}, i sent {bot_choice}',
                color = EMBED_COLOR
            ),
            mention_author = False
        )

@bot.hybrid_command (
    name = 'wordle',
    description = info_strings.help_dict['wordle']
)
@discord.app_commands.describe(practice = 'leave blank for daily wordle')
async def WORDLE(ctx, *, practice = ''):
    with open('assets/wordle_choices.txt', 'r') as f: # generates all possible words to compare against
        possible = f.read().split('\n')

    if practice.lower() in ('practice', 'new', 'true'): # you can also have a non-daily wordle solve
        with open('assets/wordle_answers.txt', 'r') as f: # generates new wordle if it's a new day
            word = random.choice(f.read().split('\n'))
        wordle_type = 'practice'
    else:
        word = DATABASE['wordle']
        wordle_type = 'daily'

    guesses = []
    formatted = []
    i = 0
    word_char_list = [*word] # splits into char array to be edited per-letter more easily

    wordle_embed = await ctx.reply ( # assigned to variable to be deleted more easily
        embed = discord.Embed (
            title = f'{wordle_type} wordle',
            description = f'type your guess below and this message will be edited accordingly',
            color = EMBED_COLOR
        ),
        mention_author = False
    )

    while i < 6: # change this number to change how many guesses are allowed
        try:
            guess = await bot.wait_for('message', timeout = 60)
            guess.content = guess.content.lower()

        except TimeoutError: # if nobody has sent a message it gets canceled
            await ctx.reply (
                embed = discord.Embed (
                    title = info_strings.error_title,
                    description = 'aborted due to inactivity',
                    color = RED_COLOR
                )
                .set_footer (
                    text = info_strings.error_clampongus,
                    icon_url = ICON_URL
                ),
                mention_author = False
            )
            break # breaks out of loop early

        try: # checks if original message exists
            await ctx.fetch_message(wordle_embed.id)
        except discord.errors.NotFound: # if the message was deleted it's treated like a cancellation
            return

        if guess.channel != ctx.channel:
            continue # ignores if message not in the same channel

        elif guess.author != ctx.author:
            continue # ignores if not from person sending message

        elif len(guess.content) != 5: # only five letter words are allowed in wordle (obviously)
            await guess.reply (
                embed = discord.Embed (
                    title = info_strings.error_title,
                    description = 'your word needs to be five characters exactly',
                    color = RED_COLOR
                )
                .set_footer (
                    text = info_strings.error_clampongus,
                    icon_url = ICON_URL
                ),
                mention_author = False
            )
            continue

        elif guess.content not in possible: # checks if it's actually a word
            await guess.reply (
                embed = discord.Embed (
                    title = info_strings.error_title,
                    description = 'that\'s not a valid word',
                    color = RED_COLOR
                )
                .set_footer (
                    text = info_strings.error_clampongus,
                    icon_url = ICON_URL
                ),
                mention_author = False
            )
            continue

        guess_char_list = [*guess.content]

        for j in range(len(guess_char_list)): # generates the colored square graphic thingy
            if guess_char_list[j] == word_char_list[j]:
                guess_char_list[j] = '🟩'
            elif guess_char_list[j] in word_char_list:
                guess_char_list[j] = '🟨'
            else:
                guess_char_list[j] = '⬜'

        guesses.append('```' + ' '.join([*guess.content]).upper() + '```\n' + ''.join(guess_char_list).upper())
        formatted = '\n'.join(i for i in guesses) # it's used in multiple places

        await wordle_embed.edit ( # edits with the new guesses
            embed = discord.Embed (
                title = wordle_embed.embeds[0].title,
                description = formatted,
                color = EMBED_COLOR
            )
        )

        i += 1

        if guess.content == word: # if you guessed the word it lets you know
            attempt = 'attempt' if i == 1 else 'attempts'
            await wordle_embed.edit (
                embed = discord.Embed (
                    title = wordle_embed.embeds[0].title,
                    description = f'you guessed the word in **{i} {attempt}**\n{formatted}',
                    color = GREEN_COLOR
                )
            )
            await guess.delete()
            return

        await guess.delete() # deletes guess after posting to save on spam

    await wordle_embed.edit ( # if you didn't get it it tells you what the word actually was
        embed = discord.Embed (
            title = wordle_embed.embeds[0].title,
            description = f'the word was **{word.upper()}**\n{formatted}',
            color = RED_COLOR
        )
    )


@bot.hybrid_command (
    name = 'behave',
    description = info_strings.help_dict['behave'],
)
async def BEHAVE(ctx):
    global deletable
    if ctx.author.id in DEVELOPER_IDS:
        deletable = False
        await ctx.reply (
            'I\'m so sorry! (⌯˃̶᷄ ﹏ ˂̶᷄⌯)',
            mention_author = False
        )
        return

    await ctx.reply (
        embed = discord.Embed (
            title = f'{ctx.author} has been banned',
            description = f'reason: ```lol no```',
            color = EMBED_COLOR
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'bean',
    description = info_strings.help_dict['bean']
)
@discord.app_commands.describe (
    member = 'who you want to b e a n',
    reason = 'i loved it when spunch bot said it was beaning time and beaned everywhere'
)
@commands.guild_only()
async def BEAN(ctx, member: discord.Member, *, reason = ''):
    if member == bot.user:
        member = ctx.author
        reason = 'trying to stop me lol'

    await ctx.reply (
        embed = discord.Embed (
            title = f'{member} has been beaned',
            description = f'reason: ```{reason}```',
            color = EMBED_COLOR
        )
        .set_footer (
            text = 'why can\'t you mention people in embed titles aaa',
            icon_url = ICON_URL
        ),
        mention_author = False
    )

@bot.hybrid_command (
    name = 'nut',
    description = info_strings.help_dict['nut'],
    aliases = ['n']
)
@discord.app_commands.describe(query = 'whether to just show the current count')
async def NUT(ctx, *, query = None):
    if query in ('total', 'amount', 'query'):
        await ctx.reply (
            embed = discord.Embed (
                title = f'total amount of NUT: **{DATABASE["nut_count"]}**',
                description = 'all fine additions to my collection',
                color = EMBED_COLOR
            ),
            mention_author = False
        )
        return

    DATABASE['nut_count'] += 1
    await write_database() # adds one to global nut count and writes it

    if DATABASE['nut_count'] % 50 == 0: # special NUT
        await ctx.reply (
            embed = discord.Embed (
                title = 'you have sacrificed a special NUT',
                description = f'you have provided the lucky {DATABASE["nut_count"]}th NUT to my collection',
                color = EMBED_COLOR
            )
            .set_footer (
                text = 'i\'m literally just checking for multiples of 50 lol',
                icon_url = ICON_URL
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
            icon_url = ICON_URL
        ),
        mention_author = False
    )

dotenv.load_dotenv() # keeps token out of public files
bot.run(os.getenv('TOKEN')) # the actual execution command