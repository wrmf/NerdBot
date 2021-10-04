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
    Moderation related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_owner)
    async def startStream(self, ctx, status: str):
        if(status is None):
            status = "Minecraft I'm sure"
        await self.bot.change_presence(activity=discord.Streaming(name=status, url="https://twitch.tv/EndermanEmerald"))

    @commands.command()
    @commands.check(is_owner)
    async def startStream(self, ctx):
        status = "Minecraft I'm sure"
        await self.bot.change_presence(activity=discord.Streaming(name=status, url="https://twitch.tv/EndermanEmerald"))

    @commands.command()
    @commands.check(is_owner)
    async def stopStream(self, ctx, status: str):
        if(status is None):
            status = "nothing, switching to JDA currently"
        await self.bot.change_presence(activity=discord.Game(name=status))

    @commands.command()
    @commands.check(is_owner)
    async def stopStream(self, ctx):
        status = "nothing, switching to JDA currently"
        await self.bot.change_presence(activity=discord.Game(name=status))

def setup(bot):
    bot.add_cog(Stream(bot))