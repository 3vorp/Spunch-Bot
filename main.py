import discord, os, wikipedia, random

### GENERAL
PREFIX = '~' # change this to change prefix
BOT_ID = '1034301829179248640' # putting this in the .env file felt pointless so here it goes
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
        if str(message.author.id) != BOT_ID and message.content[0] != PREFIX:
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


        if str(message.author.id) != BOT_ID and message.content[0] == PREFIX:
            CMD=message.content[1:] # removes the ~ part so I can change the prefix and it still works
            CMD=CMD.split( ) # splits message into each argument as a list, can be reused for all commands
            CMD[0] = CMD[0].lower() # removes case sensitivity because mobile bad

            # everything that needs prefix

            if CMD[0] == 'say':
                if len(CMD) >= 2: # this has to be in every command separately or it will remove the actual command before it gets into the condition
                    CMD.pop(0)
                    sentence=' '.join(CMD)
                    await message.delete()
                    await message.channel.send(sentence)
                else:
                    await message.channel.send('you absolute clampongus you need to actually say something') # error handling if you don't actually pass any arguments
            
            elif CMD[0] == 'wikipedia':
                if len(CMD) >= 2:
                    CMD.pop(0)
                    sentence=' '.join(CMD)
                    await message.channel.send(f'```{wikipedia.page(sentence).content[0:1900]}```')
                else:
                    await message.channel.send('you absolute clampongus you need to actually give the article')
            
            elif CMD[0] == '8ball':
                if len(CMD) >= 2:
                    CMD.pop(0)
                    sentence=' '.join(CMD)
                    await message.channel.send(f'**{sentence}**\n{random.choice(BALL_CHOICES)}') # picks random selection from BALL_CHOICES variable
                else:
                    await message.channel.send('you absolute clampongus you need to actually say something for me to respond to')

            elif CMD[0] == 'suggest' or CMD[0] == 'feedback':
                if len(CMD) >= 2:
                    CMD.pop(0)
                    sentence=' '.join(CMD)
                    await SUGGEST_CHANNEL.send(f'feedback sent by **{message.author}** in {message.channel.mention}: `{sentence}`') # formats and sends to specific channel
                    await message.channel.send('your feedback has been sent, in the meantime idk go touch grass')
                else:
                    await message.channel.send('you absolute clampongus you need to actually say something')
            
            elif CMD[0] == 'rps':
                if len(CMD) == 2:
                    CMD.pop(0)
                    sentence=''.join(CMD)
                    user_answer = sentence.lower() # formats arguments into one string

                    bot_answer=random.choice(['rock','paper','scissors']) # same concept as 8ball
                    await message.channel.send(f'you sent {user_answer}, i sent {bot_answer}')
                    if bot_answer == user_answer:
                        await message.channel.send("it's a tie")

                    elif (user_answer == 'scissors' and bot_answer == 'paper') or (user_answer == 'paper' and bot_answer == 'rock') or (user_answer == 'rock' and bot_answer == 'scissors'):
                        await message.channel.send('you win')

                    elif (user_answer == 'paper' and bot_answer == 'scissors') or (user_answer == 'rock' and bot_answer == 'paper') or (user_answer == 'scissors' and bot_answer == 'rock'):
                        await message.channel.send('i win')
                    else:
                        await message.channel.send("that wasn't an option so I automatically win :sunglasses:")
                else:
                    await message.channel.send('you either sent too much stuff or too little stuff idk too lazy to implement this message properly')

            elif CMD[0] == 'help' or CMD[0] == 'info':
                await message.channel.send (
f'''
**funny spunch bop bot** 
made by `{DEVELOPER}` because I was bored idk

*commands (more to be added soon™):*
> `{PREFIX}say`: say stuff with bot
> `{PREFIX}wikipedia`: returns wikipedia article
> `{PREFIX}8ball`: random answers for random questions
> `{PREFIX}suggest`, `{PREFIX}feedback`: suggest stuff to implement
> `{PREFIX}rps`: rock paper scissors against me
> `{PREFIX}help`, `{PREFIX}info`: shows this message, should be pretty obvious lol

*that's all for now more coming soon ig go suggest stuff to me using `{PREFIX}feedback` if you want*
''') # praise f strings 2: electric boogaloo

intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
client = main(intents=intents)

from dotenv import load_dotenv # this is so that I don't have the token directly in the file because yeah
load_dotenv() # literally googled this entire process don't ask me how it works
client.run(os.getenv("TOKEN")) # uses token from that .env file thingy to actually run the program