import discord, json, os
from discord.ext import commands

print('Loading in...')

class Ticket(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

def setup(bot):
	bot.add_cog(Ticket(bot))
	print('cogs.ticket - injected')