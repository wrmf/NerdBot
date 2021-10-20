import discord
from discord.ext import commands

from nukeIgnore import *
from bot import *
import logging
import discord
from discord.ext import commands
from bot import *
import random
import asyncio
from permissions import *
from triviaCategoriesList import triviaCategoriesList


maxTriviaQuestions = 10


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
        msg = 0

        if(category is None or category not in triviaCategoriesList):
            embed = discord.Embed(title="ERROR", description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:
            embed = discord.Embed(title="Trivia",
                                  description=f"How many questions would you like? You can have up to {maxTriviaQuestions} questions",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
            try:
                def check(m):
                    return isinstance(m, int)

                msg = await client.wait_for('message', timeout=15.0)

                if int(msg.content) < 1 or int(msg.content) > maxTriviaQuestions:
                    pass
                else:
                    embed = discord.Embed(title="ERROR",
                                          description=f"Having a trivia game with {msg.content} number of questions is not valid at the moment. Please try again and enter a number between 1 and 10.",
                                          color=ctx.message.author.top_role.color)  # Create embed
                    await ctx.send(embed=embed)  # Send embed
            except asyncio.TimeoutError:
                embed = discord.Embed(title="ERROR", description=f"Trivia Start timed out. Please try again and send a message quicker next time!",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed
                return


def setup(bot):
    bot.add_cog(Trivia(bot))