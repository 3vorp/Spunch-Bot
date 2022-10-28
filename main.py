import discord, os, wikipedia, random
from dotenv import load_dotenv # this is so that I don't have the token directly in the file because yeah

### GENERAL
PREFIX = '~' # change this to change prefix
BOT_ID = '1034301829179248640' # if you want to rebrand the bot put the bot id here so it doesn't create infinite loops and stuff
DEVELOPER = 'Evorp#5819' # idk why I included this here but who cares honestly

### FOR COMMANDS
BALL_CHOICES = ['yes','no','maybe','idk','ask later','definitely','never','never ask me that again'] # for 8ball command so it's easier to edit later

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
            await LOGGING_CHANNEL.send(f'**{message.author} ** sent `"{message.content}"` at {message.created_at} in {message.channel.mention}.')  # praise f strings


        elif message.content[0] == PREFIX:
            CONTENTS=message.content[1:].lower().split( ) # removes the prefix and any uppercase, splits contents into list
            CMD=CONTENTS[0] # gets the command portion
            CONTENTS.pop(0) # removes command from the actual contents
            SENTENCE=' '.join(CONTENTS) # use CONTENTS for list, use SENTENCE for string

            # everything that needs prefix

            if len(CONTENTS) >= 1:
                if CMD == 'say':
                    await message.delete()
                    await message.channel.send(SENTENCE)
                
                elif CMD == 'wikipedia':
                    await message.reply(f'```{wikipedia.page(SENTENCE).content[0:1900]}```', mention_author=False)
                
                elif CMD == '8ball':
                    await message.reply(f'**{SENTENCE}**\n{random.choice(BALL_CHOICES)}', mention_author=False) # picks random selection from BALL_CHOICES variable

                elif CMD == 'suggest' or CMD == 'feedback':
                    await SUGGEST_CHANNEL.send(f'feedback sent by **{message.author}** in {message.channel.mention}: `{SENTENCE}`') # formats and sends to specific channel
                    await message.reply('your feedback has been sent, in the meantime idk go touch grass', mention_author=False)
                
            elif CMD == 'rps':
                if SENTENCE == '':
                    SENTENCE=random.choice(['rock','paper','scissors'])
                bot_answer=random.choice(['rock','paper','scissors']) # same concept as 8ball
                await message.reply(f'you sent {SENTENCE}, i sent {bot_answer}', mention_author=False)
                if bot_answer == SENTENCE:
                    await message.channel.send("it's a tie")

                elif (SENTENCE == 'scissors' and bot_answer == 'paper') or (SENTENCE == 'paper' and bot_answer == 'rock') or (SENTENCE == 'rock' and bot_answer == 'scissors'):
                    await message.channel.send('you win')

                elif (SENTENCE == 'paper' and bot_answer == 'scissors') or (SENTENCE == 'rock' and bot_answer == 'paper') or (SENTENCE == 'scissors' and bot_answer == 'rock'):
                    await message.channel.send('i win')
                else:
                    await message.channel.send("that wasn't an option so I automatically win :sunglasses:")
                    
            elif CMD == 'help' or CMD == 'info':
                await message.reply (
f'''**spunch bot** 
an atrocity made in discord.py by `{DEVELOPER}` because I was bored idk

*commands (more to be added soon™):*
> `{PREFIX}say`: say stuff with bot
> `{PREFIX}wikipedia`: returns wikipedia article
> `{PREFIX}8ball`: random answers for random questions
> `{PREFIX}suggest`, `{PREFIX}feedback`: suggest stuff to implement
> `{PREFIX}rps`: rock paper scissors against me
> `{PREFIX}help`, `{PREFIX}info`: shows this message, should be pretty obvious lol

*that's all for now more coming soon ig go suggest stuff to me using `{PREFIX}feedback` if you want*
''', mention_author=False) # praise f strings 2: electric boogaloo
            else:
                await message.channel.send('you probably provided too many or too few arguments idk too lazy to implement proper error handling')

intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
client = main(intents=intents)

load_dotenv() # uses token from that .env file thingy to actually run the program
client.run(os.getenv("TOKEN")) 