import discord
import json, os
from discord.ext import commands

print('Loading in...')

class Starboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='addstar',
				aliases=['starboard'])
	@commands.has_permissions(manage_messages=True)
	async def addstar(self, ctx, emoji: str, maxcount: int=5, *args):
		re = open('json/starboard.json', 'r')
		starboard_json = json.loads(re.read())
		re.close()
		try:
			inner_json = starboard_json[str(ctx.guild.id)]
		except:
			starboard_json[str(ctx.guild.id)] = {}
			inner_json = starboard_json[str(ctx.guild.id)]
		inner_json[str(emoji)] = maxcount
		starboard_json[str(ctx.guild.id)] = inner_json
		wr = open('json/starboard.json', 'w')
		wr.write(json.dumps(starboard_json))
		wr.close()
	
	@commands.command(name='removestar',
				aliases=['unstarboard'])
	@commands.has_permissions(manage_messages=True)
	async def removestar(self, ctx, emoji: str, *args):
		re = open('json/starboard.json', 'r')
		starboard_json = json.loads(re.read())
		re.close()
		try:
			inner_json = starboard_json[str(ctx.guild.id)]
		except:
			starboard_json[str(ctx.guild.id)] = {}
			inner_json = starboard_json[str(ctx.guild.id)]
		del inner_json[str(emoji)]
		starboard_json[str(ctx.guild.id)] = inner_json
		wr = open('json/starboard.json', 'w')
		wr.write(json.dumps(starboard_json))
		wr.close()

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		print(reaction.emoji)
		re = open('json/starboard.json', 'r')
		starboard_json = json.loads(re.read())
		re.close()
		print(starboard_json)
		for i in starboard_json:
			if reaction.emoji in i:
				if reaction.count >= i[reaction.emoji]:
					print('star!')

def setup(bot):
	bot.add_cog(Starboard(bot))
	print('cogs.starboard - injected')