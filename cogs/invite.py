import discord
from discord.ext import commands
import random
from bot import *
from ids import *
from nukeIgnore import *
from permissions import *


class Invite(commands.Cog):
    """
    Nuke related commandss
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Invite the bot to your server"""

        user = ctx.author
        await user.send("My invite link is: https://tinyurl.com/yyoja52j")

def setup(bot):
    bot.add_cog(Invite(bot))