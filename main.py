import discord, os, wikipedia, random, datetime,time
from dotenv import load_dotenv # this is so that I don't have the token directly in the file because yeah

### GENERAL
PREFIX = '~' # change this to change prefix
BOT_ID = '1034301829179248640' # if you want to rebrand the bot put the bot id here so it doesn't create infinite loops and stuff
DEVELOPER = 'Evorp#5819' # idk why I included this here but who cares honestly

class main(discord.Client):
    async def on_ready(self): # starts the bot
        STARTUP_CHANNEL = client.get_channel(1034609478005436436)
        await STARTUP_CHANNEL.send(f'Online as **{self.user}**.\n——————————————') # sends startup message
        await client.change_presence(activity=discord.Game('spongeboy gif on repeat')) # discord activity

    async def on_message(self, message):
        LOGGING_CHANNEL = client.get_channel(1034329397450244136)
        SUGGEST_CHANNEL = client.get_channel(1035020903953743942)
        if str(message.author.id) == BOT_ID:
            return
        elif message.content[0] != PREFIX:
            # everything that doesn't need a prefix goes here

            if 'baller' == str(message.content).lower():
                await message.channel.send('https://cdn.discordapp.com/attachments/697947500987809846/1033358086095765504/e923830c4dbe2942417df30bf5530238.mp4')

            if 'mhhh' in str(message.content).lower():
                await message.channel.send('**mhhh**\n`uh oh moment` \nswahili → english')
                await message.channel.send('smh my head ripping off compli:b:ot very cring')
            
            if 'spongeboy' == str(message.content).lower(): 
                await message.channel.send('https://media.discordapp.net/attachments/774035111981219870/831335411787759667/pee.gif')
            
            #LOGGER
            await LOGGING_CHANNEL.send(f'**{message.author} ** sent `"{message.content}"` at <t:{message.created_at}> in {message.channel.mention} in *"{message.guild.name}"*.')  # praise f strings

        elif message.content[0] == PREFIX:
            CONTENTS=message.content[1:].lower().split( ) # removes the prefix and any uppercase, splits contents into list
            CMD=CONTENTS[0] # gets the command portion
            CONTENTS.pop(0) # removes command from the actual contents
            SENTENCE=' '.join(CONTENTS) # use CONTENTS for list, use SENTENCE for string

            # everything that needs prefix

            if len(CONTENTS) >= 1: # checks that there are arguments being passed so there's no errors, if not it will go all the way down this list and hit the else statement
                if CMD == 'say':
                    await message.delete()
                    await message.channel.send(SENTENCE) # deletes original message and sends the sentence back
                
                elif CMD == 'wikipedia':
                    try:
                        await message.reply(f'```{wikipedia.page(SENTENCE).content[0:1900]}```', mention_author=False) # this atrocity takes the input, finds wikipedia article, and trims it to 1900 characters
                    except (wikipedia.exceptions.PageError): # if there's no article with that name catches error and gives info
                        await message.reply('no wikipedia article found with that name', mention_author=False)

                elif CMD == '8ball' or CMD == 'ball':
                    await message.reply(random.choice(['yes','no','maybe','idk','ask later','definitely','never','never ask me that again']), mention_author=False) # picks random selection from these options

                elif CMD == 'suggest' or CMD == 'feedback':
                    await SUGGEST_CHANNEL.send(f'feedback sent by **{message.author}** in {message.channel.mention}: `{SENTENCE}`')
                    await message.reply('your feedback has been sent, in the meantime idk go touch grass', mention_author=False) # sends confirmation message to user
                
            elif CMD == 'rps': # needs to be outside the arguments passed if condition because the bot can automatically provide one if no arguments are passed
                if SENTENCE == '':
                    SENTENCE=random.choice(['rock','paper','scissors']) # if user provides no arguments it just randomly chooses for them

                bot_answer=random.choice(['rock','paper','scissors']) # works same way as 8ball, randomly chooses from list

                if bot_answer == SENTENCE:
                    await message.reply(f"you sent {SENTENCE}, i sent {bot_answer}:\n**it's a tie**", mention_author=False)

                elif (SENTENCE == 'scissors' and bot_answer == 'paper') or (SENTENCE == 'paper' and bot_answer == 'rock') or (SENTENCE == 'rock' and bot_answer == 'scissors'): # pain
                    await message.reply(f'you sent {SENTENCE}, i sent {bot_answer}:\n**you win**', mention_author=False)

                elif (SENTENCE == 'paper' and bot_answer == 'scissors') or (SENTENCE == 'rock' and bot_answer == 'paper') or (SENTENCE == 'scissors' and bot_answer == 'rock'): # pain II
                    await message.reply(f'you sent {SENTENCE}, i sent {bot_answer}:\n**i win**', mention_author=False)

                else:
                    await message.reply("that wasn't an option so I automatically win :sunglasses:", mention_author=False)
                    
            elif CMD == 'help' or CMD == 'info':
                await message.reply (
f'''**spunch bot** 
an atrocity made in discord.py by `{DEVELOPER}` because I was bored idk

*commands (more to be added soon™):*
> `{PREFIX}say`: say stuff with bot
> `{PREFIX}wikipedia`: returns wikipedia article
> `{PREFIX}8ball`, `{PREFIX}ball`: random answers for random questions
> `{PREFIX}suggest`, `{PREFIX}feedback`: suggest stuff to implement
> `{PREFIX}rps`: rock paper scissors against spunch bot
> `{PREFIX}help`, `{PREFIX}info`: shows this message, should be pretty obvious lol

*that's all for now more coming soon go suggest stuff to me using `{PREFIX}feedback` if you want ig*
''', mention_author=False) # praise f strings 2: electric boogaloo
            else:
                await message.reply('something went wrong (you probably sent too much stuff or not enough stuff), too lazy to implement proper errors', mention_author=False)
intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
client = main(intents=intents)

load_dotenv() # uses token from that .env file thingy to actually run the program
client.run(os.getenv("TOKEN")) 