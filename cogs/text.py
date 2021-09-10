import discord
from discord.ext import commands

from nukeIgnore import *
from bot import *
import logging
import discord
from discord.ext import commands
from bot import *
import random
from permissions import *


class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @commands.command()
        @commands.check(is_admin)
        async def echo(self, ctx: commands.Context, message: str):
            """Echo a message"""
            await ctx.channel.purge(limit=1)
            await ctx.send(message)

def setup(bot):
    bot.add_cog(Text(bot))