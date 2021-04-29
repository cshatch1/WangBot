#This code ties everything up into a neat little bow to be run
import os
import discord
import random
from keep_alive import keep_alive
from quotes import quote_list

#The token to login to the bot
TOKEN = os.getenv('DISCORD_TOKEN')

#Function that randomizes the quotes
def get_quote():
    quote = random.choice(quote_list)
    return (quote)

#Allows the script to login to the bot
class MyClient(discord.Client):
    async def on_ready(self):
        print('We have logged in as {0}'.format(self.user))

    #Prevents the bot from becoming schizophrenic and talking to itself
    async def on_message(self, message):
        if message.author == self.user:
            return

        #Check for '&q' and send a quote
        if message.content.startswith('&q'):
            quote = get_quote()
            await message.channel.send(quote)

        #Check for '&h' and send a help message
        if message.content.startswith('&h'):
          wanghelp = "Do '&q' to get a quote."
          await message.channel.send(wanghelp)

#Run the 'keep_alive.py' script and login to the bot
keep_alive()
client = MyClient()
client.run(TOKEN)
