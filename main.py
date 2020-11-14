import discord
from discord.ext import commands

import json


def open_json(filename):
	with open(f'{filename}.json', 'r') as f:
		return json.load(f)

def write_json(data, filename):
	with open(f'{filename}.json', 'w') as f:
		json.dump(data, f, indent=4)

async def send_json(ctx, filename):
	await ctx.send(f'```json\n{json.dumps(open_json(filename), indent=4)}```')


bot = commands.Bot(
	command_prefix='!',
	intents=discord.Intents.default()
)

with open('config.json', 'r') as f:
	config = json.load(f)


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

	await send_json(ctx, 'settings')


@settings.command()
async def webhook(ctx, url):
	settings = open_json('settings')
	settings["webhook"] = url
	write_json(settings, 'settings')

	await send_json(ctx, 'settings')


@settings.command()
async def channel(ctx, guild_id, channel_id):
	settings = open_json('settings')
	if "channel" not in settings:
		settings["channel"] = {}
	settings["channel"]["guild_id"] = guild_id
	settings["channel"]["channel_id"] = channel_id
	write_json(settings, 'settings')

	await send_json(ctx, 'settings')


bot.run(config["token"])
