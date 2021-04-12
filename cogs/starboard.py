import discord
import json, os
from discord.ext import commands

print('Loading in...')

class Starboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		print(reaction.message.content)
		if reaction.count

def setup(bot):
	bot.add_cog(Starboard(bot))
	print('cogs.starboard - injected')