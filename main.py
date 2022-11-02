import discord, os, wikipedia, random
from dotenv import load_dotenv # this is so that I don't have the token directly in the file because yeah
load_dotenv()

PREFIX = '~' # change this to change prefix
DEVELOPER = 'Evorp#5819' # idk why I included this here but who cares honestly
EMBED_COLOR = 0xc3ba5c # this is just a hex color code (#C3BA5C) with 0x in front of it so discord parses it as hex, idk why either
ICON = 'https://raw.githubusercontent.com/3vorp/Spunch-Bot/main/image/icon.png' # frame 106 of the spongeboy gif, probably some better way to get the icon but this works too :P

TOKEN = os.getenv("TOKEN")



class Delete_Button(discord.ui.View): # this took me so long to implement please kill me
    def __init__(self):
        super().__init__() # inheritance stuff yes yes I definitely remember stuff from OOP
    @discord.ui.button(label = 'delete', style = discord.ButtonStyle.red) # creates a red button object thingy, edit this to edit all delete buttons
    async def red_button(self,interaction:discord.Interaction,button:discord.ui.Button): # whenever button is clicked calls this function
        await interaction.message.delete()



class Main(discord.Client):
    async def on_ready(self): # starts the bot
        STARTUP_CHANNEL = client.get_channel(1034609478005436436) # hardcoded channel ids for a private server, change these if you fork this
        await STARTUP_CHANNEL.send(embed = discord.Embed(description = f'Online as {self.user.mention}',color = EMBED_COLOR)) # sends startup message
        await client.change_presence(activity=discord.Game('spongeboy gif on repeat')) # discord activity

    async def on_message(self, message):
        SUGGEST_CHANNEL = client.get_channel(1035020903953743942) # same as STARTUP_CHANNEL
        if message.author == client.user or message.content == '': # makes sure the bot can't reply to itself and cause an infinite loop
            return



        elif message.content[0] != PREFIX:
            SENTENCE = str(message.content).lower() # the .lower() is just used to remove all case sensitivity


            # everything that doesn't need a prefix goes here


            if 'baller' == SENTENCE:
                await message.reply('https://cdn.discordapp.com/attachments/697947500987809846/1033358086095765504/e923830c4dbe2942417df30bf5530238.mp4', view=Delete_Button(), mention_author=False)

            if 'mhhh' in SENTENCE: # can't use elif because it's checking if it's contained within any of the message contents
                await message.reply(embed = discord.Embed(title='mhhh', description='`uh oh moment`', color = EMBED_COLOR).set_footer(text='Swahili → English'), view=Delete_Button(), mention_author=False)
                await message.channel.send('smh my head ripping off compli:b:ot very cring') # I basically stole the joke from CompliBot/Faithful Bot so the bot calls you out on it lol
            
            if 'spongeboy' == SENTENCE:
                await message.reply('https://raw.githubusercontent.com/3vorp/Spunch-Bot/main/image/icon_big.gif', view = Delete_Button(), mention_author=False)



        elif message.content[0] == PREFIX:
            WORD_LIST=message.content[1:].lower().split( ) # removes the prefix and any uppercase, splits contents into list
            COMMAND=WORD_LIST[0] # gets the command portion
            WORD_LIST.pop(0) # removes command from the actual WORD_LIST
            SENTENCE=' '.join(WORD_LIST) # use WORD_LIST for list, use SENTENCE for string, use COMMAND for command


            # everything that needs a prefix and doesn't require arguments goes here


            if COMMAND == 'rps': # needs to be outside the arguments passed if condition because the bot can automatically provide one if no arguments are passed
                if SENTENCE == '':
                    WORD_LIST = [random.choice(['rock','paper','scissors'])] # if user provides no arguments it just randomly chooses for them

                bot_answer=random.choice(['rock','paper','scissors']) # works same way as 8ball, randomly chooses from list

                if bot_answer == WORD_LIST[0]:
                    await message.reply(embed = discord.Embed(title= "it's a tie", description=f"you sent {WORD_LIST[0]}, i sent {bot_answer}", color=EMBED_COLOR), view=Delete_Button(), mention_author=False)

                elif (WORD_LIST[0] == 'scissors' and bot_answer == 'paper') or (WORD_LIST[0] == 'paper' and bot_answer == 'rock') or (WORD_LIST[0] == 'rock' and bot_answer == 'scissors'): # pain
                    await message.reply(embed = discord.Embed(title= "you win", description=f"you sent {WORD_LIST[0]}, i sent {bot_answer}", color=EMBED_COLOR), view=Delete_Button(), mention_author=False)

                elif (WORD_LIST[0] == 'paper' and bot_answer == 'scissors') or (WORD_LIST[0] == 'rock' and bot_answer == 'paper') or (WORD_LIST[0] == 'scissors' and bot_answer == 'rock'): # pain II
                    await message.reply(embed = discord.Embed(title= "i win", description=f"you sent {WORD_LIST[0]}, i sent {bot_answer}", color=EMBED_COLOR), view=Delete_Button(), mention_author=False)

                else:
                    await message.reply(embed = discord.Embed(title="that wasn't an option so I automatically win :sunglasses:",description=f"you sent {WORD_LIST[0]}, i sent {bot_answer}",color=EMBED_COLOR), view=Delete_Button(), mention_author=False)

            elif (COMMAND == 'help' or COMMAND == 'info') and len(WORD_LIST) == 0:
                await message.reply (embed = discord.Embed(title = '**spunch bot**', description = f''' 
an atrocity made in discord.py by `{DEVELOPER}` because I was bored idk

**commands available (more to be added soon™):**

— `{PREFIX}say`: say stuff with bot
— `{PREFIX}wikipedia`: returns wikipedia article
— `{PREFIX}8ball`, `{PREFIX}ball`: random answers for random questions
— `{PREFIX}feedback`, `{PREFIX}suggest`: suggest stuff to implement
— `{PREFIX}rps`: rock paper scissors against spunch bot
— `{PREFIX}help`, `{PREFIX}info`: shows this message, should be pretty obvious lol''', color = EMBED_COLOR).set_footer(text= f"that's all for now, go suggest stuff using {PREFIX}feedback if you want me to add stuff ig",icon_url=ICON), view=Delete_Button(), mention_author=False) # praise f strings 2: electric boogaloo


            # every command that requires arguments goes here


            elif len(WORD_LIST) >= 1:  # deletes original message and sends the sentence back
                if COMMAND == 'say':
                    await message.delete()
                    await message.channel.send(message.content.partition(' ')[2]) # praise stackoverflow, I wanted to keep uppercase but just remove the first word
                
                elif COMMAND == 'wikipedia':
                    try:
                        await message.reply(f'```{wikipedia.page(SENTENCE).content[0:1900]}```', view=Delete_Button(), mention_author=False) # this atrocity takes the input, finds a wikipedia article, and trims it to 1900 characters

                    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError): # if there's no article with that name catches error and gives info
                        await message.reply(embed = discord.Embed(title = 'insert helpful error name here', description='multiple/no wikipedia article found with that name', color = EMBED_COLOR).set_footer(text="you're still an absolute clampongus though", icon_url=ICON), view=Delete_Button(), mention_author=False)

                elif COMMAND == '8ball' or COMMAND == 'ball':
                    await message.reply(embed = discord.Embed(title=SENTENCE, description=random.choice(['yes','no','maybe','idk','ask later','definitely','never','never ask me that again']), color=EMBED_COLOR), view=Delete_Button(), mention_author=False) # picks random selection from these options

                elif COMMAND == 'suggest' or COMMAND == 'feedback':
                    await SUGGEST_CHANNEL.send(embed = discord.Embed(title = f'feedback sent by **{message.author}**:', description = f'sent in {message.channel.mention}: `{SENTENCE}`', color = EMBED_COLOR)) # sends to hardcoded suggestion channel
                    await message.reply(embed = discord.Embed(title = 'your feedback has been sent', description = 'in the meantime idk go touch grass',color = EMBED_COLOR), view=Delete_Button(), mention_author=False) # sends confirmation message to user

                else:
                    await message.reply(embed = discord.Embed(title='insert helpful error name here', description="too lazy to implement proper errors but you probably sent too much stuff, not enough stuff, or something that's not a command",color=EMBED_COLOR).set_footer(text="you're still an absolute clampongus though", icon_url = ICON), view=Delete_Button(), mention_author=False) # generic error handling
                    
            else:
                await message.reply(embed = discord.Embed(title='insert helpful error name here', description="too lazy to implement proper errors but you probably sent too much stuff, not enough stuff, or something that's not a command",color=EMBED_COLOR).set_footer(text="you're still an absolute clampongus though", icon_url = ICON), view=Delete_Button(), mention_author=False) # generic error handling 2
    
intents = discord.Intents.default() # I have no idea what any of this does but it looks important so I'm not touching it
intents.message_content = True
client = Main(intents=intents)

load_dotenv() # uses token from that .env file thingy to actually run the program
client.run(TOKEN) 