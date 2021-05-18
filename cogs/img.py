import discord, json, os
from discord.ext import commands
fuck = "yes"

print('Loading in...')

def imgto(image, out_type: str='png'):
	if fuck:
		print("fuck")


class ticket_cog(commands.Cog, name='Tickets'):
	def __init__(self, bot):
		self.bot = bot

def setup(bot):
	bot.add_cog(ticket_cog(bot))
	print('cogs.ticket - injected')