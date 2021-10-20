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
from triviaCategoriesList import *


class Trivia(commands.Cog):
    """
    Trivia related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['triviaCategories'])
    async def triviaCategories(self, ctx, status: str = None):

        embed = discord.Embed(title="Trivia", description=f"The available trivia categories are:",
                              color=ctx.message.author.top_role.color) #Create embed
        i = 0
        for category in triviaCategories:
            embed.add_field(name=i, value=category, inline=True) #Set title for first embed
            i+=i
        await ctx.send(embed=embed) #Send embed

def setup(bot):
    bot.add_cog(Trivia(bot))