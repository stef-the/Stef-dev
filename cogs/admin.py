import discord, os, aiohttp, sys, contextlib, io
from subprocess import run
from discord.ext import commands
from io import StringIO

print('Loading in...')

@contextlib.contextmanager
def stdoutIO(stdout=None):
	old = sys.stdout
	if stdout is None:
		stdout = StringIO()
	sys.stdout = stdout
	yield stdout
	sys.stdout = old

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='console', pass_context=True, hidden=True)
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
	
	@commands.command(name='eval', aliases=['evaluate', 'ev'], pass_context=True, hidden=True)
	@commands.is_owner()
	async def eval(self, ctx, *args):
		str_obj = io.StringIO()
		try:
			with contextlib.redirect_stdout(str_obj):
				exec(' '.join(args))
			output = str_obj.getvalue()
			
			try:
				await ctx.reply(str(output), mention_author=False)

			except:
				session = aiohttp.ClientSession()
				async with session.post("https://hst.sh/documents", data=output) as resp:
					body = await resp.json()
					print(body)
					output = "https://hst.sh/" + body['key']
				await session.close()
				await ctx.reply(str(output), mention_author=False)
		except Exception as e:
			await ctx.reply(f'<:error:830635116048810005> Error while Executing script: \n```py\n{" ".join(args)}\n```\n**Error:** ```py\n{e}\n```', mention_author=False)

		


def setup(bot):
	bot.add_cog(Admin(bot))
	print('cogs.admin - injected')