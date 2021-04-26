import discord, os, json
from discord.ext import commands

print('Loading in...')

class Leveling(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='level', 
					pass_context=True,
					aliases=['rank', 'lvl'],
					description='Check your global and server levels/message count.\n**Example:** -level <@648316569059065859>')
	@commands.has_permissions(ban_members=True)
	@commands.guild_only()
	async def level(self, ctx, user: discord.Member=None):
		read = open('json/leveling.json', 'r')
		leveling_json = json.loads(read.read())
		read.close()

		if user == None:
			author_id = str(ctx.author.id)
		else:
			author_id = str(user.id)

		guild_id = str(ctx.guild.id)

		total_user_msg = leveling_json[author_id]
		guild_user_msg = leveling_json[guild_id][author_id]

		embed = discord.Embed()
		embed.title = 'Leveling'
		embed.description = f'Server Messages: `{guild_user_msg}`\nGlobal Messages: `{total_user_msg}`'

		slvl = None
		glvl = None
		gfn = False
		tfn = False

		global i
		for i in range(0, 999):
			lvl_msg = (i / 2) * (i / 2) * 100
			if guild_user_msg <= lvl_msg and not gfn:
				glvl = i - 1
				print(glvl)
				gfn = True
				if tfn:
					break
			if total_user_msg <= lvl_msg and not tfn:
				slvl = i - 1
				print(slvl)
				tfn = True
				if gfn:
					break

		if slvl == None:
			slvl = 0
		
		if glvl == None:
			glvl = 0

		embed.add_field(name="User Level", value=f'Global Level: `{slvl}`\nGuild Level: `{glvl}`', inline=False)

		await ctx.reply(embed=embed, mention_author=False)

	@commands.Cog.listener()
	async def on_message(self, message):
		read = open('json/leveling.json', 'r')
		leveling_json = json.loads(read.read())
		read.close()

		author_id = str(message.author.id)
		guild_id = str(message.guild.id)

		if not message.author.bot:

			try:
				leveling_json[author_id] += 1
			except:
				leveling_json[author_id] = 1
			
			try:
				leveling_json[guild_id][author_id] += 1
			except:
				leveling_json[guild_id] = {}
				leveling_json[guild_id][author_id] = 1
		
			total_user_msg = leveling_json[author_id]
			guild_user_msg = leveling_json[guild_id][author_id]

		write = open('json/leveling.json', 'w')
		write.write(json.dumps(leveling_json))
		write.close()

def setup(bot):
	bot.add_cog(Leveling(bot))
	print('cogs.leveling - injected')