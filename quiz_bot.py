# quiz_bot.py
# implement main bot fuctionality

import os
import discord
from db_utils import db_utils
from discord.ext import commands
from dotenv import load_dotenv
from datetime import date


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
dbu = db_utils()


# on ready is called when the bot logs in
# BUG: this function gives diagnostic error 
#   "guild is possibly unbound?"
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


@bot.command(pass_context = True)
async def whoami(ctx):
    """Returns username, id"""
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )
    await ctx.send(msg)


@bot.command()
async def questions(ctx, class_spec="none"):
    if class_spec == "none":
        return
    return


@bot.command(pass_context = True)
async def SetUpUser(ctx):
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )
    await ctx.send(msg)


@bot.command()
async def AddClass(ctx, class_name="none"):
    if class_name == "none":
        return
    dbu.add_class(class_name)
    return


@bot.command()
async def AddTopic(ctx, topic_name="none"):
    if topic_name == "none":
        return
    dbu.add_topic(topic_name) 
    return


@bot.command()
async def AddQuestion(ctx, topic_name="none"):
    #TODO: figure out how to extract topic
    return


#TODO: implement answer question


#TODO: implement get question


#TODO: implement get answers
    

bot.run(TOKEN)
