import discord, json, os
from discord.ext import commands

print('Loading in...')

class Status(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='status', pass_context=True, hidden=True, aliases=['st'])
	@commands.is_owner()
	async def status(self, ctx, s_type='', *args):
		status_types = {
			"watching": ['watch', 'watching'],
			"playing": ['play', 'playing'],
			"listening": ['listen', 'listening'],
			"streaming": ['stream', 'streaming'],
			"idle": ['idle'],
			"online": ['online', 'on'],
			"dnd": ['dnd', 'donotdisturb'],
			"offline": ['offline', 'off', 'invis', 'invisible'],
			"clear": ['none', 'clear']
		}
		item = True
		stype = s_type.lower()
		if stype in status_types['clear']:
			embed = discord.Embed(title='Status Change', description=f'Status was cleared.')
			activity = None
		elif stype in status_types['watching']:
			embed = discord.Embed(title='Status Change', description=f'Status was set to `Watching {" ".join(args)}`.')
			activity = discord.Activity(type=discord.ActivityType.watching, name=" ".join(args))
		elif stype in status_types['playing']:
			embed = discord.Embed(title='Status Change', description=f'Status was set to `Playing {" ".join(args)}`.')
			activity = discord.Game(name=" ".join(args))
		elif stype in status_types['listening']:
			embed = discord.Embed(title='Status Change', description=f'Status was set to `Listening {" ".join(args)}`.')
			activity = discord.Activity(type=discord.ActivityType.listening, name=" ".join(args))
		elif stype in status_types['streaming']:
			e = []
			for i in args:
				if not args[0] == i:
					e.append(i)
			embed = discord.Embed(title='Status Change', description=f'Status was set to **`Streaming `**`{" ".join(args)}`.')
			activity=discord.Streaming(name=" ".join(e), url=args[0])
		else:
			item = False

		if item:
			await ctx.reply(embed=embed, mention_author=False)
			await self.bot.change_presence(activity=activity)


def setup(bot):
	bot.add_cog(Status(bot))
	print('cogs.status - injected')