import discord
import os
from discord.ext import commands

print('Loading in...')

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	@commands.is_owner()
	async def load(self, ctx, module : str):
		try:
			self.bot.load_extension(module)
			await ctx.reply(f'<:yes:830635069222813766> Cog `{module}` was loaded.', mention_author=False)
		except Exception as e:
			await ctx.reply(f'<:error:830635116048810005> Error while loading extension: ```py\n{e}\n```', mention_author=False)

	@commands.command(hidden=True)
	@commands.is_owner()
	async def unload(self, ctx, module : str):
		try:
			self.bot.unload_extension(module)
			await ctx.reply(f'<:yes:830635069222813766> Cog `{module}` was unloaded.', mention_author=False)
		except Exception as e:
			await ctx.reply(f'<:error:830635116048810005> Error while loading extension: ```py\n{e}\n```', mention_author=False)

	@commands.command(hidden=True, name='reload')
	@commands.is_owner()
	async def _reload(self, ctx, module : str):
		try:
			self.bot.unload_extension(module)
			self.bot.load_extension(module)
			await ctx.reply(f'<:yes:830635069222813766> Cog `{module}` was reloaded.', mention_author=False)
		except Exception as e:
			await ctx.reply(f'<:error:830635116048810005> Error while loading extension: ```py\n{e}\n```', mention_author=False)

def setup(bot):
	bot.add_cog(Admin(bot))
	print('cogs.admin - injected')