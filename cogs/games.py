import discord
from discord.ext import commands
import random
from bot import *
from permissions import *
import asyncio

blankSquare = '|'️
xSquare = 'X'️
circleSquare = 'O'️

def getCircle(ctx, user):
    embed = discord.Embed(title="TicTacToe",
                          description=f"User {user.mention} would you like to be circle or cross?",
                          color=ctx.message.author.top_role.color)  # Create error embed
    await ctx.send(embed=embed)  # Send embed
    def check(message: discord.Message):  # Check for getting the number of questions
        return message.channel == ctx.channel and message.author == user and (message.clean_content.lower() ==
                                                            'circle' or message.clean_content.lower() == 'cross')
    try:
        msg = await client.wait_for('message', timeout=30, check=check)  # Get response from user
        if 'circle' not in msg.clean_content.lower():
            embed = discord.Embed(title="TicTacToe",
                                  description=f"User {user.mention} has selected circle. {ctx.message.author.mention} "
                                              f"will be cross",
                                  color=ctx.message.author.top_role.color)  # Create error embed
            await ctx.send(embed=embed)  # Send embed
            return user
        elif 'cross' not in msg.clean_content.lower():
            embed = discord.Embed(title="TicTacToe",
                                  description=f"User {user.mention} has selected cross. {ctx.message.author.mention} "
                                              f"will be circle",
                                  color=ctx.message.author.top_role.color)  # Create error embed
            await ctx.send(embed=embed)  # Send embed
            return ctx.message.author
    except asyncio.TimeoutError:  # Timeout
        embed = discord.Embed(title="ERROR",
                              description=f"User {user.mention} did not select a symbol. Ending game",
                              color=ctx.message.author.top_role.color)  # Create error embed
        await ctx.send(embed=embed)  # Send embed
        return None

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

        def check(message: discord.Message): #Check for getting the number of questions
            return message.channel == ctx.channel and message.author == user
        try:
            msg = await client.wait_for('message', timeout=30, check=check)  # Get response from user
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

        embed = discord.Embed(title="Success!",
                              description=f"User {user.mention} accepted your challenge! Generating board!",
                              color=ctx.message.author.top_role.color)  # Create error embed
        gameMessage = await ctx.send(embed=embed)  # Send embed

        embed.set_footer(text='ID: {}'.format(gameMessage.id))

        circleUser = getCircle(ctx, user)
        await ctx.send(f"The user that selected circle is {circleUser.mention}")



def setup(bot):
    bot.add_cog(Games(bot))