import discord
import json, os
from discord.ext import commands
from discord.utils import get

print('Loading in...')

class Starboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='starchannel',
				aliases=['starch'])
	@commands.has_permissions(manage_messages=True)
	async def starchannel(self, ctx, channel: discord.TextChannel=None, *args):
		re = open('json/starboard.json', 'r')
		starboard_json = json.loads(re.read())
		re.close()
		if channel == None:
			channel = ctx.channel
		inner_json = starboard_json[str(ctx.guild.id)]
		inner_json["channel"] = channel.id
		starboard_json[str(ctx.guild.id)] = inner_json
		wr = open('json/starboard.json', 'w')
		wr.write(json.dumps(starboard_json))
		wr.close()

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
		for i in starboard_json:
			e = starboard_json[i]
			try:
				if not reaction.emoji.id:
					if e[reaction.emoji] <= reaction.count:
						thing = True
				else:
					if e[f'<:{reaction.emoji.name}:{reaction.emoji.id}>'] <= reaction.count:
						thing = True
				if thing:
					embed = discord.Embed(title=f'Starboard - {reaction.emoji}', description=f'[Message]({reaction.message.jump_url}) by {reaction.message.author.mention} / `{reaction.message.author.id}`')
					embed.add_field(name="Message Content", value=reaction.message.content, inline=False)
					channel = discord.utils.get(reaction.message.guild.channels, id=e["channel"])
					await channel.send(embed=embed)	
			except:
				return

def setup(bot):
	bot.add_cog(Starboard(bot))
	print('cogs.starboard - injected')