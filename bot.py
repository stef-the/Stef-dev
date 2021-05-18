import discord, discord_slash
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from discord.ext import commands

def get_prefix(bot, message):
	prefixes = ['-']

	if not message.guild:
		return('?')
	
	return(commands.when_mentioned_or(*prefixes)(bot, message))

bot = commands.Bot(command_prefix=get_prefix, description='...')
slash = SlashCommand(bot)

import sys, traceback, os, json, datetime

initial_extensions = ['cogs.admin', 'cogs.moderation', 'cogs.starboard', 'cogs.status', 'cogs.leveling']

if __name__ == '__main__':
	for extension in initial_extensions:
		print('\n')
		bot.load_extension(extension)

@bot.event
async def on_ready():

	global client
	client = bot.user

	print(f'\n\nLogging in as: {client.name} - {client.id}\ndiscord.py version: {discord.__version__}\ndiscord_slash version: {discord_slash.__version__}\njson version: {json.__version__}\n')
	print(f'Successfully logged in.')

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, module : str):
	try:
		bot.load_extension(module)
		await ctx.reply(f'<:yes:830635069222813766> Cog `{module}` was loaded.', mention_author=False)
	except Exception as e:
		await ctx.reply(f'<:error:830635116048810005> Error while loading extension: ```py\n{e}\n```', mention_author=False)

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, module : str):
	try:
		bot.unload_extension(module)
		await ctx.reply(f'<:yes:830635069222813766> Cog `{module}` was unloaded.', mention_author=False)
	except Exception as e:
		await ctx.reply(f'<:error:830635116048810005> Error while loading extension: ```py\n{e}\n```', mention_author=False)

@bot.command(hidden=True, name='reload')
@commands.is_owner()
async def _reload(ctx, module : str):
	try:
		bot.unload_extension(module)
		bot.load_extension(module)
		await ctx.reply(f'<:yes:830635069222813766> Cog `{module}` was reloaded.', mention_author=False)
	except Exception as e:
		await ctx.reply(f'<:error:830635116048810005> Error while loading extension: ```py\n{e}\n```', mention_author=False)

@bot.command(hidden=True, name='cogs')
@commands.is_owner()
async def cogs(ctx, folder: str='cogs'):
	try:
		if os.listdir(f'./{folder}'):
			print('.')
		item = True
	except:
		await ctx.reply('<:error:830635116048810005> Folder not found.', mention_author=False)
		item = False
	
	if item:
		e = []
		thing = 0
		for i in os.listdir(f'./{folder}'):
			if i.endswith('.py'):
				b = i.replace('.py', '')
				try:
					print('\n')
					bot.load_extension(f"{folder}.{b}")
					bot.unload_extension(f"{folder}.{b}")
					e.append(f'<:off:830634812842442772> `{i}` - unloaded')
					thing += 1
				except commands.ExtensionAlreadyLoaded:
					e.append(f'<:on:830634662912589837> `{i}` - loaded')
					thing += 1
		embed = discord.Embed(title=f'Cogs ({thing})', description='\n'.join(e))
		await ctx.reply(embed=embed, mention_author=False)

@bot.command(name='shutdown', 
			hidden=True)
async def shutdown(ctx):
	print("<SHUTDOWN> Start")
	try:
		await bot.close()
		print("<SHUTDOWN> Successful")
	except Exception as e:
		print(f"<SHUTDOWN> EnvironmentError as {e}")
		bot.clear()

class MyNewHelp(commands.MinimalHelpCommand):
	async def send_pages(self):
		destination = self.get_destination()
		for page in self.paginator.pages:
			embed = discord.Embed(title='Help', description=page)
			await destination.send(embed=embed)	

bot.help_command = MyNewHelp()

@bot.command(name='ping',
			aliases=['pong'],
			definition='Check the bot\'s response time.\n**Example:** -ping')
async def ping(ctx):
	await ctx.reply(f'🏓 Pong! `{round((bot.latency * 1000), 4)}ms`', mention_author=False)

@bot.command(name='info',
			aliases=['i', 'information'],
			definition='Information about the bot.\n**Example:** -info')
async def info(ctx):
	embed = discord.Embed(title='Information', description=f'')
	embed.add_field(name='Module Versions', value=f'`discord.py` version: {discord.__version__}\n`discord_slash` version: {discord_slash.__version__}\n`json` version: {json.__version__}\n', inline=False)
	await ctx.reply(embed=embed, mention_author=False)

@bot.event
async def on_message(message):
		try:
			await bot.process_commands(message)

		except Exception as e:
			append = open('log/all.log', 'a')
			append.write(e)
			append.close()
from os import getenv

token = open('.env', 'r').read().replace('TOKEN=', '') #os.getenv('TOKEN')
bot.run(token, bot=True, reconnect=True)