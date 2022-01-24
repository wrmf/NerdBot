import discord
from discord.ext import commands

from nukeIgnore import *
from bot import *
import logging
import discord
from discord.ext import commands
from bot import *
import random
from ids import *
from permissions import *


class Text(commands.Cog):
    """
    Text related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_owner)
    async def echo(self, ctx: commands.Context, message: str, num: int = 1):
        """
        Echo a message
        @author Nerd#2022
        """
        
        counter = 0

        await ctx.channel.purge(limit=1)  # Delete original message

        while counter < num:
            await ctx.send(message) #Send message
            counter+=1

    @commands.command()
    @commands.check(is_owner)
    async def dm(self, ctx: commands.Context, id: int, message: str, num: int = 1):
        """
        Direct message a user a message
        @author Nerd#2022
        """

        counter = 0

        await ctx.channel.purge(limit=1)  # Delete original message

        while counter < num:
            user = await ctx.guild.fetch_member(id)
            await user.send(message) #Send message
            counter+=1



def setup(bot):
    bot.add_cog(Text(bot))