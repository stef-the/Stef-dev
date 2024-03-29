import discord, os, aiohttp
from discord.ext import commands

print('Loading in...')

class admin_cog(commands.Cog, name='Admin'):
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
	
	@commands.command(name='evaluate',
					pass_context=True, 
					hidden=True, 
					aliases=['ev', 'eval'])
	@commands.is_owner()
	async def evaluate(self, ctx, *args):
		try:
			output = eval(' '.join(args))
		except Exception as e:
			output = e
		embed = discord.Embed()
		embed.title='Evaluate'
		embed.description=f'**Input:**```py\n{" ".join(args)}```**Output:**```py\n{output}```'
		await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
	bot.add_cog(admin_cog(bot))
	print('cogs.admin - injected')