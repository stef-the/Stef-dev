import discord, json, os, requests
from discord.ext import commands
from PIL import Image

print('Loading in...')

class testing(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def img(self, ctx, to:str):
		corrects = ['png', 'ico', 'jpg']
		img1 = ctx.message.attachments[0]
		postfix = img1.filename.split('.')[1]
		print(postfix)

		r = requests.get(img1.url, allow_redirects=True)
		open('temp.' + postfix, 'wb').write(r.content)

		if postfix in corrects:
			if to in corrects:
				img = Image.open(img1.filename)
				img.save(rf'send.{to}')
				img = None

				await ctx.reply(file=discord.File(rf'send.{to}'), mention_author=False)
				os.remove(rf'send.{to}')
			
		os.remove('temp.' + postfix)

def setup(bot):
	bot.add_cog(testing(bot))
	print('cogs.img-stef - injected')