import discord, json, os
from discord.ext import commands

print('Loading in...')

class ticket_cog(commands.Cog, name='Tickets'):
	def __init__(self, bot):
		self.bot = bot

def setup(bot):
	bot.add_cog(ticket_cog(bot))
	print('cogs.ticket - injected')