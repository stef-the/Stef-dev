import discord, json, os
from discord.ext import commands
from PIL import Image

print('Loading in...')

def imgto(image: dict=None, out_type:str='png'):
	if image['name'].endswith('.png'):
		return(False)

class testing(commands.Cog, name='Tickets'):
	def __init__(self, bot):
		self.bot = bot

def setup(bot):
	bot.add_cog(testing(bot))
	print('cogs.img-stef - injected')