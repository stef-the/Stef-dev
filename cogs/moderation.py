import discord, json, os
from discord.ext import commands
from discord.utils import get

print('Loading in...')

class moderation_cog(commands.Cog, name='Moderation'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='ban', 
					pass_context=True,
					aliases=['banish'],
					description='Ban a user from your Guild.\nRequires `ban_members` permission.\n**Example:** -ban <@648316569059065859> He did something bad')
	@commands.has_permissions(ban_members=True)
	@commands.guild_only()
	async def ban(self, ctx, user: discord.Member, *args):
		reason = f'{ctx.author} / {ctx.author.id} | '
		reason += " ".join(args)
		if user:
			try:
				await user.ban(reason=reason)
				return_msg = f"<:yes:830635069222813766> Banned user `{user.mention}`"
				if args:
					return_msg += f" for reason `{' '.join(args)}`"
				return_msg += "."
				await ctx.reply(return_msg, mention_author=False)
			except discord.Forbidden:
				await ctx.reply('<:error:830635116048810005> Could not ban user. Try checking my permissions, or message the devs.', mention_author=False)
		else:
			await ctx.reply('<:no:830635025187209216> Could not find user.', mention_author=False)
	
	@commands.command(name='kick', 
					pass_context=True,
					description='Kick a member in your Guild.\nRequires `kick_members` permission.\n**Example:** -kick <@648316569059065859> He did something bad')
	@commands.has_permissions(kick_members=True)
	@commands.guild_only()
	async def kick(self, ctx, user: discord.Member, *args):
		reason = f'{ctx.author} / {ctx.author.id} | '
		reason += " ".join(args)
		if user:
			try:
				await user.kick(reason=reason)
				return_msg = "<:yes:830635069222813766> Kicked user `{user.mention}`"
				if args:
					return_msg += f" for reason `{' '.join(args)}`"
				return_msg += "."
				await ctx.reply(return_msg, mention_author=False)
			except discord.Forbidden:
				await ctx.reply('<:error:830635116048810005> Could not ban user. Try checking my permissions, or message the devs.', mention_author=False)
		else:
			await ctx.reply('<:no:830635025187209216> Could not find user.', mention_author=False)

	@commands.command(name='purge',
					pass_context=True,
					description='Purge messages in your Guild.\nRequires `manage_messages` permission.\n**Examples:** -purge 20 Stef e (purges the 20 last messages sent by Stef with the letter `e`), -purge 20 (purges 20 messages).')
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, msgs: int, members="everyone", *, txt=None):
		await ctx.message.delete()
		member_object_list = []
		if members != "everyone":
			member_list = [x.strip() for x in members.split(",")]
			for member in member_list:
				if "@" in member:
					member = member[3 if "!" in member else 2:-1]
				if member.isdigit():
					member_object = ctx.guild.get_member(int(member))
				else:
					member_object = ctx.guild.get_member_named(member)
				if not member_object:
					return await ctx.send(self.bot.bot_prefix + "Invalid user.")
				else:
					member_object_list.append(member_object)

		if msgs < 10000:
			async for message in ctx.message.channel.history(limit=msgs):
				try:
					if txt:
						if not txt.lower() in message.content.lower():
							continue
					if member_object_list:
						if not message.author in member_object_list:
							continue

					await message.delete()
				except discord.Forbidden:
					await ctx.send(self.bot.bot_prefix + f"You do not have permission to delete other users' messages. Use {self.bot.cmd_prefix}delete instead to delete your own messages.")
		else:
			await ctx.send(self.bot.bot_prefix + 'Too many messages to delete. Enter a number < 10000')

	@kick.error
	async def kick_error(ctx, error):
		text = f"<:no:830635025187209216> {ctx.author.mention} - Missing `kick_members` permission"
		await ctx.reply(text, mention_author=False)
	
	@purge.error
	async def purge_error(ctx, error):
		text = f"<:no:830635025187209216> {ctx.author.mention} - Missing `manage_messages` permissions"
		await ctx.reply(text, mention_author=False)
	
	@ban.error
	async def ban_error(ctx, error):
		text = f"<:no:830635025187209216> {ctx.author.mention} - Missing `ban_members` permissions"
		await ctx.reply(text, mention_author=False)

def setup(bot):
	bot.add_cog(moderation_cog(bot))
	print('cogs.moderation - injected')