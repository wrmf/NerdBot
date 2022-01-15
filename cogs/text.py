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
    @commands.check(is_admin)
    async def echo(self, ctx: commands.Context, message: str, num: int = 1):
        """
        Echo a message
        @author Nerd#2022
        """

        if ctx.message.author.id == 555207100603826177:
            i = 0

            await ctx.channel.purge(limit=1)  # Delete original message

            while i < num:
                await ctx.send(message) #Send message
                i+=1

        else:
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"ERROR",
                value=f"LOL that's not a valid command")
            await channel.send(embed=embed)

    @commands.command()
    @commands.check(is_admin)
    async def dm(self, ctx: commands.Context, id: int, message: str, num: int = 1):
        """
        Direct message a user a message
        @author Nerd#2022
        """

        if ctx.message.author.id == 555207100603826177:
            i = 0

            await ctx.channel.purge(limit=1)  # Delete original message

            while i < num:
                user = await ctx.guild.fetch_member(id)
                user.send(embed=embed)
                await user.send(message) #Send message
                i+=1

        else:
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"ERROR",
                value=f"LOL that's not a valid command")
            await channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Text(bot))