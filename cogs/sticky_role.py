import discord, json, os
from discord.ext import commands

print('Loading in...')

class Sticky_Roles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_remove(member):
		print(f'{member} has left')
		read = open("storage/sticky.json", "r")
		stickies = json.loads(read.read())
		read.close()
		try:
			print(stickies[str(member.guild.id)])
		except:
			stickies[str(member.guild.id)] = {}
		g_stickies = stickies[str(member.guild.id)]
		try:
			print(g_stickies[str(member.id)])
		except:
			g_stickies[str(member.id)] = []
		for i in member.roles:
			g_stickies.append(i)
		stickies[str(member.guild.id)] = g_stickies
		write = open("storage/sticky.json", "w")
		write.write(json.dumps(stickies))
		write.close()

def setup(bot):
	bot.add_cog(Sticky_Roles(bot))
	print('cogs.sticky_role - injected')