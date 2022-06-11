import discord
from discord.ext import commands
import random
from bot import *
from permissions import *
import asyncio

def generateNewBoard():
    pass


class Games(commands.Cog):
    """
    Game commands
    @author Nerd#2022
    """

    @commands.command()
    @commands.guild_only()
    async def challenge(self, ctx: commands.Context, user: discord.Member = None):
        """
        Challenges a user to TicTacToe. Format: ~challenge @user
        """

        await ctx.send(f"{user.mention}, {ctx.message.author.mention} has challenged you to TicTacToe. "
                       f"If you accept, please type 'yes' in the next 30 seconds")

        def check(message: discord.Message, originalChannelID: int, originalAuthorID: int): #Check for getting the number of questions
            return message.channel == ctx.channel
        try:
            msg = await client.wait_for('message', timeout=10, check=check)  # Get response from user
            if 'yes' not in msg.clean_content.lower():
                embed = discord.Embed(title="ERROR",
                                      description=f"User {user.mention} did not say yes. Ending game",
                                      color=ctx.message.author.top_role.color)  # Create error embed
                await ctx.send(embed=embed)  # Send embed
                return None
        except asyncio.TimeoutError:  # Timeout
            embed = discord.Embed(title="ERROR",
                                  description=f"User {user.mention} did not respond. Ending game",
                                  color=ctx.message.author.top_role.color)  # Create error embed
            await ctx.send(embed=embed)  # Send embed
            return None

        embed = discord.Embed(title="ERROR",
                              description=f"User {user.mention} accepted your challenge! Generating board!",
                              color=ctx.message.author.top_role.color)  # Create error embed
        await ctx.send(embed=embed)  # Send embed

def setup(bot):
    bot.add_cog(Games(bot))