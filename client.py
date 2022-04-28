# bot.py

import os
import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


# on ready is called when the bot logs in
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )

    for member in guild.members:
        print(member)


# on message is called when a message is received on the server
@client.event
async def on_message(message):
    if message.content.startswith('!hello'):
        await message.channel.send('trash')
    if message.content.startswith('!questions'):
        # for
        return


client.run(TOKEN)
