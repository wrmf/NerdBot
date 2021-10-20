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
    async def triviaStart(self, ctx, category: str = None):

        if(category is None or category not in triviaCategoriesList):
            embed = discord.Embed(title="ERROR", description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:
            embed = discord.Embed(title="Trivia",
                                  description=f"How many questions would you like? You can have up to 10 questions",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
            try:
                msg = await client.wait_for('messsage', timeout=15.0)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="ERROR",
                                      description=f"",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed
                return

def setup(bot):
    bot.add_cog(Trivia(bot))