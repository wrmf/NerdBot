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
    """
    Text related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_admin)
    async def echo(self, ctx: commands.Context, message: str):
        """
        Echo a message
        @author Nerd#2022
        """

        await ctx.channel.purge(limit=1) #Delete original message
        await ctx.send(message) #Send message

def setup(bot):
    bot.add_cog(Text(bot))