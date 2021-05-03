import discord, json, os
from discord.ext import commands

print('Loading in...')

class nopo_cog(commands.Cog, name='Nopo\'s Cog'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='mods',
				aliases=['mod'],
				description='View the list of Nopo\'s mods!\n**Example:** -mod patcher')
	async def mods(self, ctx, Mod: str=None):
		m = open('nopo/mods.json', 'r')
		mods = json.loads(m.read())
		m.close()
		if not Mod:
			embed = discord.Embed(title='Nopo\'s Mods')
			tick = 0
			for mod in mods:
				tick += 1
				embed.add_field(name=mod["display"], value=f'[Download]({mod["download_url"]}) - [Github]({mod["github"]}) - [Discord](https://discord.gg/{mod["discord_code"]})', inline=True)
			embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/TEgFEX3gvvGbPXTPa82suzAugE461g5Fs3XGafIqTdI/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/384620942577369088/a7a569e104b8bc391a73a3dc5d2e8962.png')
			await ctx.reply(embed=embed, mention_author=False)
		else:
			try:
				for mod in mods:
					for item in mod['nicks']:
						if Mod.lower() == item.lower():
							mstr = str(mod["nicks"]).replace("[", "").replace("]", "").replace("'", "`")
							embed = discord.Embed(title=mod['display'], description=f'Aliases: {mstr}\nVersion: `{mod["version"]}`', url=mod['url'])
							embed.set_thumbnail(url=mod['icon_url'])
							embed.set_footer(text=mod['creator'], icon_url=mod['creator_icon'])
							embed.add_field(name='Description', value=mod['description'], inline=False)
							embed.add_field(name='URLs',value=f'[Download]({mod["download_url"]}) - [Github]({mod["github"]}) - [Discord](https://discord.gg/{mod["discord_code"]})', inline=False)
				await ctx.reply(embed=embed, mention_author=False)
			except Exception as e:
				print(e)
				await ctx.reply(content="<:s_dnd:822236762771554315> Please send a valid mod.", mention_author=False)

	@commands.command(name='packs',
				aliases=['pack', 'resourcepack', 'texturepack'],
				description='View the list of Nopo\'s packs!\n**Example:** -pack sbov')
	async def packs(self, ctx, Pack: str=None):
		m = open('nopo/packs.json', 'r')
		mods = json.loads(m.read())
		m.close()
		if not Pack:
			embed = discord.Embed(title='Nopo\'s Packs')
			tick = 0
			for mod in mods:
				tick += 1
				embed.add_field(name=mod["display"], value=f'[Download]({mod["download_url"]}) - [Github]({mod["github"]}) - [Discord](https://discord.gg/{mod["discord_code"]})', inline=True)
			embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/TEgFEX3gvvGbPXTPa82suzAugE461g5Fs3XGafIqTdI/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/384620942577369088/a7a569e104b8bc391a73a3dc5d2e8962.png')
			await ctx.reply(embed=embed, mention_author=False)
		else:
			try:
				for mod in mods:
					for item in mod['nicks']:
						if Pack.lower() == item.lower():
							mstr = str(mod["nicks"]).replace("[", "").replace("]", "").replace("'", "`")
							embed = discord.Embed(title=mod['display'], description=f'Aliases: {mstr}\nVersion: `{mod["version"]}`', url=mod['url'])
							embed.set_thumbnail(url=mod['icon_url'])
							embed.set_footer(text=mod['creator'], icon_url=mod['creator_icon'])
							embed.add_field(name='Description',value=mod['description'], inline=False)
							embed.add_field(name='URLs',value=f'[Download]({mod["download_url"]}) - [Github]({mod["github"]}) - [Discord](https://discord.gg/{mod["discord_code"]})', inline=False)
				await ctx.reply(embed=embed, mention_author=False)
			except Exception as e:
				print(e)
				await ctx.reply(content="<:s_dnd:822236762771554315> Please send a valid pack.", mention_author=False)

def setup(bot):
	bot.add_cog(nopo_cog(bot))
	print('cogs.nopo - injected')