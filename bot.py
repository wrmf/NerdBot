import json
import random

import discord
from ids import *
from ldl_staff import *
from ldl_channels import *
from ownerPrefix import *
import signal
import discord.opus
import asyncio
from discord.ext.commands import AutoShardedBot, when_mentioned_or, Context
from tokenfile import token
import logging
import os
from possibleMessages import possibleMessages
import pandas as pd
import datetime


airportCodesTriviaDataframe = None


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
		#await context.send(f'{exception}')
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
		if msg.guild.me in msg.mentions:
			if ctx.message.author.id == TNMN:
				pass
			elif ctx.message.author.id == Cheese:
				embed = discord.Embed(title="PING",
									  description=possibleMessages[random.randint(0, len(possibleMessages) - 1)], #Correct answer,
									  color=ctx.message.author.top_role.color)  # Create error embed
				embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer

				await ctx.send(embed=embed)  # Send embed
			else:
				embed = discord.Embed(title="PING",
									  description=f"My prefix is ~. You can get my command list by doing ~help",
									  color=ctx.message.author.top_role.color)  # Create error embed
				embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
				await ctx.send(embed=embed)  # Send embed

		if "nayle" in msg.clean_content.lower():
			if(ctx.guild.id == NAYLE_2021_staff):
				await ctx.send("NAYLE? I love NAYLE!")

		if "outpost" in msg.clean_content.lower():
			if(ctx.guild.id == NAYLE_2021_staff):
				await ctx.send("ARE WE THERE YET?")

		if "christopher " in msg.clean_content.lower() or "chris " in msg.clean_content.lower():
			if(ctx.guild.id == LDL_server and ctx.message.author.id == 538719895186047006 or ctx.message.author.id == TNMN):
				await ctx.channel.purge(limit=1)
				user = await ctx.guild.fetch_member(868928903878697020)
				embed = discord.Embed(color=ctx.author.color.value)
				embed.add_field(name="**ERROR**", value=f"{ctx.message.author.mention} called you {msg.clean_content}",
								inline=True)
				await user.send(embed=embed)

		if ctx.message.author.id == 609355069212852244 and ctx.message.guild.id == 707226419993772112:
			if random.randint(0,20) == 0:
				await ctx.send(ctx.message.content)

		if "good bot" in msg.clean_content:
			await ctx.send("beep boop")

		if "bee" in msg.clean_content.lower() and msg.channel.id in [710542883375022160, 829711652382441503, 901267588041044059]:
			await ctx.send("https://cdn.discordapp.com/attachments/710544037198823454/932073503224627300/IMG_3040.webp")

		if "uwu" in msg.clean_content.lower() and ctx.message.guild.id == LDL_server:
			await ctx.send("Stop it. Get some help")

		for m in msg.mentions:
			if await self.is_owner(m) and not await self.is_owner(msg.author):
				if(not ctx.guild.id == NAYLE_2021_staff):
					await msg.add_reaction("<:pingsock:638087023269380126>")

		for m in msg.mentions:
			if(ctx.guild.id == LDL_server):
				if(ctx.author.id in ldl_staff[0] or ctx.channel.id in ldl_channels[0]):
					pass
				else:
					if(m.id == Lockdown):
						if ctx.message.author.id == 191221766625034240 or ctx.message.author.id == 272413868033179649:
							embed = discord.Embed(color=ctx.message.author.top_role.color.value)
							embed.add_field(name=f"Bruh", value=f"Bruh")
							await ctx.send(embed=embed)

						user = ctx.message.author
						await ctx.send(f"{user.mention} please refrain from pinging Lockdown! Feel free to ping any admin or mod if you have a question! **WARNING**")
						channel = discord.utils.get(user.guild.channels, name="logs")
						embed = discord.Embed(color=ctx.message.author.top_role.color.value)
						embed.add_field(
							name=f"Moderation",
							value=f"{user.mention} pinged lockdown! **WARNING**")
						await channel.send(embed=embed)

		for m in msg.mentions:
			if(ctx.guild.id == LDL_server):
				if(ctx.author.id in ldl_staff[0] or ctx.channel.id in ldl_channels[0]):
					pass
				else:
					beginningDate = datetime.datetime(2022, 4, 1)
					endDate = datetime.datetime(2022, 5, 1)
					currentDate = datetime.datetime.today()
					if(m.id == Cheese and currentDate >= beginningDate and currentDate <= endDate):
						await ctx.send(f"{ctx.message.author.mention} Cheese is on a break. Please do not disturb them.")

client = Bot(prefix=when_mentioned_or('~' if 'prefix' not in options else options['prefix']),
			 pm_help=True if 'pm_help' not in options else options['pm_help'],
			 activity = discord.Game('nothing. Banging my head against a wall at JDA currently' if 'game' not in options else options['game']))

async def get_pre(bot, message):
	pre = ["~"]

	is_owner = await bot.is_owner(message.author)
	if isinstance(message.channel, discord.DMChannel) or (is_owner and not owner_no_prefix):
		pre.append("")

async def signal_handler(signal, frame):
  await ctx.send("E")

signal.signal(signal.SIGINT, signal_handler)


@client.event
async def on_ready():
	print('--------------------')
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('--------------------')

	# Read in CSV for airport code trivia
	columns = ["Name", "ID"]  # Columns for pandas array
	LDLStaffDataframe = pd.read_csv("ldl_staffText.csv", header=None, delimiter="(", names=columns)
	LDLStaffDataframe["ID"] = LDLStaffDataframe["ID"].str[:-1]  # Delete ) from end of string
	LDLStaffDataframe.sort_values("Name")  # Sort values by code... does this do anything?


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.load_extension("jishaku")

client.run(token)
