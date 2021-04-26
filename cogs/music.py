import re, os, discord, lavalink
from discord.ext import commands

print('Loading in...')
url_rx = re.compile(r'https?://(?:www\.)?.+')

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		if not hasattr(bot, 'lavalink'):
			bot.lavalink = lavalink.Client(804096162097004544)
			bot.lavalink.add_node('42.54.191.92', 1295, 'pog', 'eu', 'default-node')  # Host, Port, Password, Region, Name
			bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')
		
		lavalink.add_event_hook(self.track_hook)

	def cog_unload(self):
		self.bot.lavalink._event_hooks.clear()

	async def cog_before_invoke(self, ctx):

		guild_check = ctx.guild is not None

		if guild_check:
			await self.ensure_voice(ctx)

		return guild_check

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			await ctx.reply(error.original, mention_author=False)

	async def ensure_voice(self, ctx):
		player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))

		should_connect = ctx.command.name in ('play')

		if not ctx.author.voice or not ctx.author.voice.channel:
			raise commands.CommandInvokeError('<:no:830635025187209216> Join a Voice Channel first')

		if not player.is_connected:
			if not should_connect:
				raise commands.CommandInvokeError('<:no:830635025187209216> Not connected')

			permissions = ctx.author.voice.channel.permissions_for(ctx.me)

			if not permissions.connect or not permissions.speak:
				raise commands.CommandInvokeError('<:no:830635025187209216> I need the `CONNECT` and `SPEAK` permissions')

			player.store('channel', ctx.channel.id)
			await ctx.guild.change_voice_state(channel=ctx.author.voice.channel)
		else:
			if int(player.channel_id) != ctx.author.voice.channel.id:
				raise commands.CommandInvokeError('<:no:830635025187209216> You need to be in my Voice Channel')
	
	async def track_hook(self, event):
		if isinstance(event, lavalink.events.QueueEndEvent):
			guild_id = int(event.player.guild_id)
			guild = self.bot.get_guild(guild_id)
			await guild.change_voice_state(channel=None)

	@commands.command(name='play',
					aliases=['pl', 'p'],
					definition='Play a song. Uses Lavalink.\n**Example:** -play Never Gonna Give You Up')
	async def play(self, ctx, *, query: str):
		player = self.bot.lavalink.player_manager.get(ctx.guild.id)
		
		query = query.strip('<>')

		if not url_rx.match(query):
			query = f'ytsearch:{query}'

		results = await player.node.get_tracks(query)

		if not results or not results['tracks']:
			return await ctx.send('Nothing found!')

		embed = discord.Embed(color=discord.Color.blurple())

		#   TRACK_LOADED	- single video/direct URL)
		#   PLAYLIST_LOADED - direct URL to playlist)
		#   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
		#   NO_MATCHES	  - query yielded no results
		#   LOAD_FAILED	 - most likely, the video encountered an exception during loading.

		if results['loadType'] == 'NO_MATCHES':
			embed.title = '<:no:830635025187209216> No Match'
			embed.description = f'Could not find a song or playlist associated with `{query}`.'

		elif results['loadType'] == 'LOAD_FAILED':
			embed.title = '<:no:830635025187209216> Error'
			embed.description = f'Error while loading song `{query}`.'

		elif results['loadType'] == 'PLAYLIST_LOADED':
			tracks = results['tracks']

			for track in tracks:
				player.add(requester=ctx.author.id, track=track)

			embed.title = '<:yes:830635069222813766> Playlist Queued'
			embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'

		else:
			track = results['tracks'][0]
			embed.title = '<:yes:830635069222813766> Track Queued'
			embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

			track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
			player.add(requester=ctx.author.id, track=track)

		await ctx.reply(embed=embed, mention_author=False)

		if not player.is_playing:
			await player.play()

	@commands.command(name='disconnect',
					aliases=['dc', 'leave', 'stop'],
					description='Disconnect from a VC when playing music.\n**Example:** -disconnect')
	async def disconnect(self, ctx):
		player = self.bot.lavalink.player_manager.get(ctx.guild.id)

		if not player.is_connected:
			return await ctx.reply('<:no:830635025187209216> Not connected to a Voice Channel', mention_author=False)

		if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
			return await ctx.reply('<:no:830635025187209216> You\'re not in my Voice Channel!', mention_author=False)

		player.queue.clear()

		await player.stop()
		await ctx.guild.change_voice_state(channel=None)
		await ctx.reply('<:yes:830635069222813766> Disconnected', mention_author=False)
	
	@commands.command(name='pause',
					description='Pause / Resume music that is currently playing. Same functionnality as -resume command.\n**Example:** -pause')
	async def pause(self, ctx):
		player = self.bot.lavalink.player_manager.get(ctx.guild.id)

		if not player.is_connected:
			return await ctx.reply('<:no:830635025187209216> Not connected to a Voice Channel', mention_author=False)

		if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
			return await ctx.reply('<:no:830635025187209216> You\'re not in my Voice Channel!', mention_author=False)

		if player.paused:
			await player.set_pause(False)
			await ctx.reply('<:yes:830635069222813766> Unpaused', mention_author=False)
		
		elif not player.paused:
			await player.set_pause(True)
			await ctx.reply('<:yes:830635069222813766> Paused', mention_author=False)
	
	@commands.command(name='resume',
					description='Resume / Pause music that is currently playing. Same functionnality as -resume command.\n**Example:** -resume')
	async def resume(self, ctx):
		player = self.bot.lavalink.player_manager.get(ctx.guild.id)

		if not player.is_connected:
			return await ctx.reply('<:no:830635025187209216> Not connected to a Voice Channel', mention_author=False)

		if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
			return await ctx.reply('<:no:830635025187209216> You\'re not in my Voice Channel!', mention_author=False)

		if player.paused:
			await player.set_pause(False)
			await ctx.reply('<:yes:830635069222813766> Unpaused', mention_author=False)
		
		elif not player.paused:
			await player.set_pause(True)
			await ctx.reply('<:yes:830635069222813766> Paused', mention_author=False)
	
	@commands.command(name='volume', aliases=['vol', 'v'])
	async def volume(self, ctx, volume: int=None):
		player = self.bot.lavalink.player_manager.get(ctx.guild.id)

		if not player.is_connected:
			return await ctx.reply('<:no:830635025187209216> Not connected to a Voice Channel', mention_author=False)

		if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
			return await ctx.reply('<:no:830635025187209216> You\'re not in my Voice Channel!', mention_author=False)

		if volume == None:
			await ctx.reply(f'Current volume is `{player.volume}%`', mention_author=False)

		elif volume < 1000 and volume >= 0:
			oldvol = player.volume
			await player.set_volume(volume)
			await ctx.reply(f'<:yes:830635069222813766> Volume was set from `{oldvol}%` to `{volume}%`', mention_author=False)

		else:
			await ctx.reply(f'<:no:830635025187209216> Make sure your volume is an int in between 0 and 1000', mention_author=False)


def setup(bot):
	bot.add_cog(Music(bot))
	print('cogs.moderation - injected')