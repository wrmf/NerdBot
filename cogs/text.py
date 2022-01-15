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
    async def echo(self, ctx: commands.Context, message: str, num: int = 1):
        """
        Echo a message
        @author Nerd#2022
        """

        i = 0

        await ctx.channel.purge(limit=1)  # Delete original message

        while i < num:
            await ctx.send(message) #Send message
            i+=1

def setup(bot):
    bot.add_cog(Text(bot))