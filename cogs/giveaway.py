import discord
from discord.ext import commands
import random
from bot import *
from permissions import *

class Giveaway(commands.Cog):
    """
    Giveaway commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(is_admin)
    async def giveaway(self, ctx: commands.Context, item: str):
        """
        Create a giveaway
        """

        reaction = '🎉'

        embed = discord.Embed(title="Giveaway!", description=item+f"\n\n Hosted by {ctx.message.author.mention}")
        react_message = await ctx.send(embed=embed)
        await react_message.add_reaction(reaction)
        embed.set_footer(text='Giveaway ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)


    @commands.command(pass_context=True)
    @commands.check(is_admin)
    async def roll(self, ctx: commands.Context, id):
        giveaway_message = await ctx.fetch_message(id)
        if not giveaway_message.embeds:
            return
        voters = [ctx.me.id]  # add the bot's ID to the list of voters to exclude it's votes

        for reaction in giveaway_message.reactions:
            reactors = await reaction.users().flatten()
            for reactor in reactors:
                if reactor.id not in voters:
                    voters.append(reactor.id)
        if(ctx.message.author.id != ctx.me.id):
            voters.remove(ctx.me.id)
        voters.remove(giveaway_message.author.id)
        if (len(voters) <= 0):
            embed = discord.Embed(title="ERROR", description=f"No one has entered this giveaway!\n\n Hosted by {ctx.message.author.mention}",
                                  color=ctx.message.author.top_role.color)
            await ctx.send(embed=embed)
            return
        winner_id = str(voters[random.randint(0, len(voters) - 1)])
        await ctx.send("Congrats on winning <@" + winner_id + ">!")

        try:
            embed = discord.Embed(title="Giveaway ended!",description="Winner: <@" + winner_id + f">!\n\n Hosted by {ctx.message.author.mention}")
            embed.set_footer(text='Giveaway ID: {}'.format(giveaway_message.id))
            await giveaway_message.edit(embed=embed)
        except discord.forbidden:
            embed = discord.Embed(title="ERROR", description=f"Giveaway was not hosted by {ctx.me.mention}. I cannot edit the embed")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Giveaway(bot))