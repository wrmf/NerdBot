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

        reaction = '🎉' #Reaction that you want the giveaway to be with

        embed = discord.Embed(title="Giveaway!", description=item+f"\n\n Hosted by {ctx.message.author.mention}") #Create embed
        react_message = await ctx.send(embed=embed) #Send original giveaway message
        await react_message.add_reaction(reaction) #React with the reaction
        embed.set_footer(text='Giveaway ID: {}'.format(react_message.id)) #Add giveaway ID (message.id)
        await react_message.edit(embed=embed) #Edit the emebd with the giveaway ID


    @commands.command(pass_context=True)
    @commands.check(is_admin)
    async def roll(self, ctx: commands.Context, id):
        """Roll a giveaway"""
        giveaway_message = await ctx.fetch_message(id) #Set what message is the giveaway

        #Check if giveaway has an embed
        if not giveaway_message.embeds:
            return

        voters = [ctx.message.author.id]  # add the bot's ID to the list of voters to exclude it's votes

        #Add the IDs of all of the people that have entered
        for reaction in giveaway_message.reactions:
            reactors = await reaction.users().flatten()
            for reactor in reactors:
                if reactor.id not in voters:
                    voters.append(reactor.id)

        voters.remove(giveaway_message.author.id) #Remove author of poll (so that the bot doesn't win)

        #Send an error if no one has entered the giveaway
        if (len(voters) <= 0):
            embed = discord.Embed(title="ERROR", description=f"No one has entered this giveaway!\n\n Hosted by {ctx.message.author.mention}",
                                  color=ctx.message.author.top_role.color)
            await ctx.send(embed=embed)
            return

        winner_id = str(voters[random.randint(0, len(voters) - 1)]) #Get the ID of the winner
        await ctx.send("Congrats on winning <@" + winner_id + ">!") #Send message pinging winner

        #Edit original message so it's not still advertising a giveaway
        try:
            embed = discord.Embed(title="Giveaway ended!",description="Winner: <@" + winner_id + f">!\n\n Hosted by {ctx.message.author.mention}")
            embed.set_footer(text='Giveaway ID: {}'.format(giveaway_message.id))
            await giveaway_message.edit(embed=embed)
        #Error if bot can't edit embed
        except discord.Forbidden:
            embed = discord.Embed(title="ERROR", description=f"Giveaway was not hosted by {ctx.me.mention}. I cannot edit the embed")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Giveaway(bot))