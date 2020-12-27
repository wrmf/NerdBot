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

		####
		#PC#
		####

		PC = 555087033652215830
		bot_testing = 610630587275018250
		bot_spam = 555583505246060555
		discord_bots = 593298949977407508
		mod_discussions = 580951068985393175
		actionlog = 751484616128331859
		modlog = 751485850361004143
		warnings = 593294730381492225

		bot_spam_TC = 609514186753441802
		nerf = 617514604913885415

		BTH = 617992443668987914

		spam = 620067136735281202
		off_topic = 620067149502873610

		#######
		#HPWPH#
		#######

		HPWPH = 709871237937102869
		autopostHPWPH = 748198688798802050
		mod_channelHPWPH = 748922203030159462

		########
		#People#
		########

		TNMN = 555207100603826177

		discordWebsite = ["discord.gg"]
		testeta = ["test1234"]


		if msg.guild.me in msg.mentions:
			if(ctx.message.author.id == TNMN):
				pass
			else:
				await ctx.send("My prefix is -. You can get my command list by doing -help")

		for m in msg.mentions:
			if await self.is_owner(m) and not await self.is_owner(msg.author):
				if(ctx.guild.id == 787387679703695410):
					await ctx.send("Please stop pinging me damnit")
				else:
					await msg.add_reaction("<:pingsock:638087023269380126>")






client = Bot(prefix=when_mentioned_or('-' if 'prefix' not in options else options['prefix']),
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
