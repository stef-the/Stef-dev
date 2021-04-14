import discord, os, aiohttp
from subprocess import run
from discord.ext import commands

print('Loading in...')

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='console', pass_context=True, hidden=True)
	@commands.is_owner()
	async def console(self, ctx, *args):
		item = os.popen(' '.join(args)).readlines()
		output = eval(str(item)[1:-1])
		try:
			await ctx.reply(output, mention_author=False)
		except Exception as e:
			session = aiohttp.ClientSession()
			async with session.post("https://hst.sh/documents", data="your content") as resp:
				body = await resp.json()
				print("https://hst.sh/" + body.key)
			print('large! ' + e)


def setup(bot):
	bot.add_cog(Admin(bot))
	print('cogs.admin - injected')