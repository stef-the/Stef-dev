import discord, os, aiohttp
from discord.ext import commands

print('Loading in...')

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='console',
					pass_context=True, 
					hidden=True, 
					aliases=['sh', 'shell'])
	@commands.is_owner()
	async def console(self, ctx, *args):
		item = os.popen(' '.join(args)).readlines()
		output = '\n'.join(eval(str(item)))
		try:
			await ctx.channel.send(output)
		except:
			session = aiohttp.ClientSession()
			async with session.post("https://hst.sh/documents", data=output) as resp:
				body = await resp.json()
				output = "https://hst.sh/" + body['key']
			await session.close()
			await ctx.reply(str(output), mention_author=False)

def setup(bot):
	bot.add_cog(Admin(bot))
	print('cogs.admin - injected')