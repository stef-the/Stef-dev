import discord, json, os, requests
from discord.ext import commands, tasks

print('Loading in...')

class sbov(commands.Cog, name='SBOV Cog'):
	def __init__(self, bot):
		self.bot = bot

	async def downloadcount():
		try:
			testchannel = self.bot.get_channel(838790855779287181)
		except Exception as e:
			testchannel = None
		try:
			mainchannel = self.bot.get_channel(838790786958491648)
		except Exception as e:
			mainchannel = None
		
		gitapi = requests.get('https://api.github.com/repos/skyblock-overhaul/skyblock-overhaul-website-v2/releases')
		gitjson = gitapi.json()
		print(gitjson)
		
		


def setup(bot):
	bot.add_cog(sbov(bot))
	downloadcount.start()
	print('cogs.download_count - injected')