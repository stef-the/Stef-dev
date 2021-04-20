import re

import discord
import lavalink
from discord.ext import commands

url_rx = re.compile(r'https?://(?:www\.)?.+')


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		if not hasattr(bot, 'lavalink'):
			bot.lavalink = lavalink.Client(804096162097004544)
			bot.lavalink.add_node('lava2.danbot.host', 2333, 'DBH', 'us', 'default-node')  # Host, Port, Password, Region, Name
			bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

		lavalink.add_event_hook(self.track_hook)

	def cog_unload(self):
		""" Cog unload handler. This removes any event hooks that were registered. """
		self.bot.lavalink._event_hooks.clear()

	async def cog_before_invoke(self, ctx):
		""" Command before-invoke handler. """
		guild_check = ctx.guild is not None

		if guild_check:
			await self.ensure_voice(ctx)
			#  Ensure that the bot and command author share a mutual voicechannel.

		return guild_check

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send(error.original)
			# The above handles errors thrown in this cog and shows them to the user.
			# This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
			# which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
			# if you want to do things differently.

	async def ensure_voice(self, ctx):
		""" This check ensures that the bot and command author are in the same voicechannel. """
		player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
		# Create returns a player if one exists, otherwise creates.
		# This line is important because it ensures that a player always exists for a guild.

		# Most people might consider this a waste of resources for guilds that aren't playing, but this is
		# the easiest and simplest way of ensuring players are created.

		# These are commands that require the bot to join a voicechannel (i.e. initiating playback).
		# Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
		should_connect = ctx.command.name in ('play',)

		if not ctx.author.voice or not ctx.author.voice.channel:
			raise commands.CommandInvokeError('Join a Voice Channel first.')

		if not player.is_connected:
			if not should_connect:
				raise commands.CommandInvokeError('Not connected.')

			permissions = ctx.author.voice.channel.permissions_for(ctx.me)

			if not permissions.connect or not permissions.speak:  # Check user limit too?
				raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

			player.store('channel', ctx.channel.id)
			await ctx.guild.change_voice_state(channel=ctx.author.voice.channel)
		else:
			if int(player.channel_id) != ctx.author.voice.channel.id:
				raise commands.CommandInvokeError('You need to be in my voicechannel.')

	async def track_hook(self, event):
		if isinstance(event, lavalink.events.QueueEndEvent):
			# When this track_hook receives a "QueueEndEvent" from lavalink.py
			# it indicates that there are no tracks left in the player's queue.
			# To save on resources, we can tell the bot to disconnect from the voicechannel.
			guild_id = int(event.player.guild_id)
			guild = self.bot.get_guild(guild_id)
			await guild.change_voice_state(channel=None)

	@commands.command(aliases=['pl'])
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

	@commands.command(aliases=['dc'])
	async def disconnect(self, ctx):
		""" Disconnects the player from the voice channel and clears its queue. """
		player = self.bot.lavalink.player_manager.get(ctx.guild.id)

		if not player.is_connected:
			# We can't disconnect, if we're not connected.
			return await ctx.send('Not connected.')

		if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
			# Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
			# may not disconnect the bot.
			return await ctx.send('You\'re not in my voicechannel!')

		# Clear the queue to ensure old tracks don't start playing
		# when someone else queues something.
		player.queue.clear()
		# Stop the current track so Lavalink consumes less resources.
		await player.stop()
		# Disconnect from the voice channel.
		await ctx.guild.change_voice_state(channel=None)
		await ctx.send('*⃣ | Disconnected.')


def setup(bot):
	bot.add_cog(Music(bot))