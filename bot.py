import discord, discord_slash
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from discord.ext import commands

def get_prefix(bot, message):
	prefixes = ['-']

	if not message.guild:
		return '?'
	
	return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description='Very Very cool bot!')
slash = SlashCommand(bot)

import sys, traceback, os, json

initial_extensions = ['cogs.admin', 'cogs.nopo', 'cogs.moderation']

if __name__ == '__main__':
    for extension in initial_extensions:
		print('\n')
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\ndiscord.py version: {discord.__version__}\n')
    print(f'Successfully logged in.')


token = os.getenv('token')
bot.run(token, bot=True, reconnect=True)