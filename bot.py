import json
import logging
import os
import re

import discord.opus
from discord.ext.commands import AutoShardedBot, when_mentioned_or, Context
from discord.ext.commands import CommandNotFound

from tokenfile import token
#from words import cussWords

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='NerdBot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
logger.info('=== RESTART ===')

with open("options.json") as f:
	options = json.loads(f.read())


class Bot(AutoShardedBot):
	def __init__(self, *args, prefix=None, **kwargs):
		super().__init__(prefix, *args, **kwargs)

	async def on_command_error(self, context, exception):
		await context.send(f'{exception}')
		logging.error(exception)

	async def on_message(self, msg: discord.Message):
		if not self.is_ready() or msg.author.bot:
			return

		logger.debug(f'{msg}: {msg.clean_content} [{msg.system_content}]')

		ctx = await self.get_context(msg)

		try:
			await self.process_commands(msg)
			if 'delete_orig' in options and options['delete_orig'] and isinstance(ctx, Context) and ctx.valid:
				await msg.delete()
		except BaseException as e:
			logger.error(repr(e))

		########
		#People#
		########

		TNMN = 555207100603826177
		Lockdown = 703964837578932234


		if msg.guild.me in msg.mentions:
			if(ctx.message.author.id == TNMN):
				pass
			else:
				await ctx.send("My prefix is ~. You can get my command list by doing ~-help")

		for m in msg.mentions:
			if await self.is_owner(m) and not await self.is_owner(msg.author):
				await msg.add_reaction("<:pingsock:638087023269380126>")

		for m in msg.mentions:
			if(ctx.guild.id == 707226419993772112):
				if(m.id == Lockdown):
					user = ctx.message.author
					await ctx.send(f"{user.mention} please refrain from pinging Lockdown! Feel free to ping any admin or mod if you have a question! **WARNING**")
					channel = discord.utils.get(user.guild.channels, name="logs")
					embed = discord.Embed(color=ctx.message.author.top_role.color.value)
					embed.add_field(
						name=f"Moderation",
						value=f"{user.mention} pinged lockdown! **WARNING**")
					await channel.send(embed=embed)







client = Bot(prefix=when_mentioned_or('~' if 'prefix' not in options else options['prefix']),
			 pm_help=True if 'pm_help' not in options else options['pm_help'],
			 activity=discord.Game(
				 'with python' if 'game' not in options else options['game']))

@client.event
async def on_ready():
	print('--------------------')
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('--------------------')

for file in os.listdir("cogs"):
	if file.endswith(".py"):
		name = file[:-3]
client.load_extension(f"cogs.{name}")

client.load_extension("jishaku")

client.run(token)
