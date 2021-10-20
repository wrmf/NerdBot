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
from triviaCategoriesList import triviaCategoriesList


class Trivia(commands.Cog):
    """
    Trivia related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['triviacategories'])
    async def triviaCategories(self, ctx):

        embed = discord.Embed(title="Trivia", description=f"The available trivia categories are:",
                              color=ctx.message.author.top_role.color) #Create embed
        i = 1
        for category in triviaCategoriesList:
            embed.add_field(name=i, value=category, inline=True) #Set title for first embed
            i+=i
        await ctx.send(embed=embed) #Send embed

    @commands.command(aliases=['triviastart'])
    async def triviaStart(self, ctx, *category: str):

        if(category is None or category not in triviaCategoriesList):
            embed = discord.Embed(title="ERROR", description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:
            await ctx.send("idk I haven't gotten this far in my coding yet leave me alone")

def setup(bot):
    bot.add_cog(Trivia(bot))