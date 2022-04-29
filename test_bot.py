# bot.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import date


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# on ready is called when the bot logs in
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )

    for member in guild.members:
        print(member)


@bot.command()
async def get_date(ctx):
    await ctx.send(date.today())


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def repeat(ctx, times: int, content="repeating..."):
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def repeat2(ctx, times: int, content="repeating..."):
    msg = ""
    for i in range(times):
        msg += content + "\n"

    await ctx.send(msg)


bot.run(TOKEN)
