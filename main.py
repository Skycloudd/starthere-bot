import discord
from discord.ext import commands

import json
import requests

from utility_functions import *


DEBUG = False


bot = commands.Bot(
    command_prefix='!',
    intents=discord.Intents.default()
)

config = open_json('config')


@bot.event
async def on_ready():
    game = discord.Game("updating #start-here")
    await bot.change_presence(activity=game, status=discord.Status.online)
    print('Ready')


@bot.event
async def on_message(message):
    app_info = await bot.application_info()

    if message.author.id != app_info.owner.id:
        return

    await bot.process_commands(message)


@bot.group()
async def settings(ctx):
    pass


@settings.command()
async def github(ctx, url):
    settings = open_json('settings')
    settings["github"] = url
    write_json(settings, 'settings')


@bot.command()
async def update(ctx, channel: discord.TextChannel):
    if not DEBUG:
        settings = open_json('settings')
        github_url = settings["github"]

    webhooks = await channel.webhooks()
    webhook = webhooks[0]
    if not DEBUG:
        r = requests.get(github_url)
        data = json.loads(r.text)
    else:
        with open('starthere.json', 'r') as f:
            data = json.load(f)

    embeds = [discord.Embed.from_dict(i) for i in data["embeds"]]

    if not DEBUG:
        async for message in webhook.channel.history(limit=None):
            await message.delete()

    await webhook.send(
        content=data["content"],
        username=data["username"],
        avatar_url=data["avatar_url"],
        embeds=embeds
    )

    await ctx.send('Updated!')

bot.run(config["token"])
