import discord, os
from discord.ext import commands

print('Loading in...')

class GitHub(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	


def setup(bot):
	bot.add_cog(GitHub(bot))
	print('cogs.github - injected')