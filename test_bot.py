# test_bot.py
# test bot provides random test commands

import os
import asyncio
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
bot.count = 1


# on ready is called when the bot logs in
# BUG: this function gives a diagnostic error that guild is possibly unbound?
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

bot.thumb_count = 0

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    if payload.emoji.name == '👍':
        bot.thumb_count += 1
        msg = (
                f'thumbs up received\n'
                f'thumb count: {bot.thumb_count}'
                )
        await channel.send(msg)

@bot.command()
async def pick(ctx):
    bot.count += 1
    await ctx.send(f'counter at {bot.count}')

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


#same as repeat but sends all in one message
@bot.command()
async def repeat2(ctx, times: int, content="repeating..."):
    msg = ""
    for i in range(times):
        msg += content + "\n"
    await ctx.send(msg)


@bot.command()
async def whoami(ctx):
    msg = (
        f'name: {ctx.message.author.name}\n'
        f'id: {ctx.message.author.id}\n'
    )
    await ctx.send(msg)


# discord async get input after command
# takes a specified prompt and timeout, returns reply (or times out)
async def get_input(ctx, message, timeout=5):
    await ctx.send(message)

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=timeout) # 30 seconds to reply
        return msg.content
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        return 0


@bot.command()
async def AddQuestion(ctx, topic_name="none"):
    #TODO: figure out how to extract topic
    if topic_name == "none":
        await ctx.send("Command requires topic name --> ex. '!AddQuestion relational algebra'")
    else:
        msg = await get_input(ctx, "what's the question?")

    if msg != 0:
        await ctx.send(f'you said {msg}')


@bot.command()
async def AddClassTopic(ctx, *args):
    if len(args) == 0:
        err_msg = (
            f'Command requires class name: !AddClassTopic cpsc231\n'
            f'You can also add optional list of arguments: !AddClassTopic cpsc231 java oo polymorphism'
        )
        await ctx.send(err_msg)
    else:
        test_msg = ""
        for index,arg in enumerate(args):
            if index == 0:
                test_msg += f'class name: {arg}\n'
            else:
                test_msg += f'class topic: {arg}\n'
        await ctx.send(test_msg)

    return


bot.run(TOKEN)




