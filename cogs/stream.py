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


class Stream(commands.Cog):
    """
    Stream related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['startstream'])
    @commands.check(is_owner)
    async def startStream(self, ctx, status: str = None):
        """
        Change bot's status to streaming
        @author Nerd#2022
        """

        #Make sure bot doesn't error when no status is given
        if(status is None):
            status = "Minecraft I'm sure"

        await self.bot.change_presence(activity=discord.Streaming(name=status,
                                                                  url="https://twitch.tv/EmerqldEnderman")) #Set status
        embed = discord.Embed(title="Stream", description=f"Status has been updated to streaming!",
                              color=ctx.message.author.top_role.color) #Create embed
        await ctx.send(embed=embed) #Send embed

    @commands.command(aliases=['stopstream'])
    @commands.check(is_owner)
    async def stopStream(self, ctx, status: str = None):
        """
        Change bot's status from streaming
        @author Nerd#2022
        """

        #Make sure bot doesn't error when no status is given
        if(status is None):
            status = "nothing, I'm not switching to JDA"

        await self.bot.change_presence(activity=discord.Game(name=status)) #Set status
        embed = discord.Embed(title="Stream", description=f"Bot's status is no longer streaming",
                              color=ctx.message.author.top_role.color) #Create embed
        await ctx.send(embed=embed) #Send embed

def setup(bot):
    bot.add_cog(Stream(bot))