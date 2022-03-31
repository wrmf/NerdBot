import discord
from discord.ext import commands
import random
from bot import *
from permissions import *

class Giveaway(commands.Cog):
    """
    Giveaway commands
    @author Nerd#2022
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(is_admin)
    async def giveaway(self, ctx: commands.Context, item: str):
        """
        Create a giveaway
        @param item: item being given away
        @author Nerd#2022
        """

        reaction = '🎉' #Reaction that you want the giveaway to be with

        embed = discord.Embed(title="Giveaway!", description=item+f"\n\n Hosted by {ctx.message.author.mention}") #Create embed
        react_message = await ctx.send(embed=embed) #Send original giveaway message
        await react_message.add_reaction(reaction) #React with the reaction
        embed.set_footer(text='Giveaway ID: {}'.format(react_message.id)) #Add giveaway ID (message.id)
        await react_message.edit(embed=embed) #Edit the emebd with the giveaway ID


    @commands.command(pass_context=True)
    @commands.check(is_admin)
    async def roll(self, ctx: commands.Context, id, numWinners: int = 1):
        """
        Roll a giveaway
        @param id: giveaway message ID
        @param numWinners: number of winners for the giveaway to have
        @author Nerd#2022
        """
        user = ctx.message.author
        giveaway_message = await ctx.fetch_message(id) #Set what message is the giveaway

        #Check if giveaway has an embed
        if not giveaway_message.embeds:
            await user.send(f"Sorry, embed {id} is not a valid giveaway. "
                            f"If you believe this is a mistake, please contact Nerd#2022")
            return
        #Send an error if number of winners is less than 1 (a giveaway with negative winners??)
        elif numWinners < 1:
            embed = discord.Embed(title="ERROR",
                                  description=f"You cannot roll a giveaway with less than one winner!\n\n"
                                              f" Hosted by {ctx.message.author.mention}",
                                  color=ctx.message.author.top_role.color)
            await user.send(embed=embed)

        voters = [ctx.message.author.id]  # add the bot's ID to the list of voters to exclude it's votes

        #Add the IDs of all of the people that have entered
        for reaction in giveaway_message.reactions:
            reactors = await reaction.users().flatten()
            for reactor in reactors:
                if reactor.id not in voters:
                    voters.append(reactor.id)

        voters.remove(giveaway_message.author.id) #Remove author of poll (so that the bot doesn't win)

        #Correct number of winnners of there are supposed to be more winners than the number of people that entered
        if numWinners > len(voters):
            numWinners = len(voters)

        #Send an error if no one has entered the giveaway
        if (len(voters) <= 0):
            embed = discord.Embed(title="ERROR", description=f"No one has entered this giveaway!\n\n Hosted by {ctx.message.author.mention}",
                                  color=ctx.message.author.top_role.color)
            await ctx.send(embed=embed)
            return

        i = 0
        winner_id = []
        winner_users = []

        #Get the winners (can be more than 1)
        if numWinners > 1:
            while i < numWinners:
                winner_id_temp = str(voters[random.randint(0, len(voters) - 1)]) #Get the ID of the winner
                while winner_id_temp in winner_id:
                    winner_id_temp = str(voters[random.randint(0, len(voters) - 1)]) #Get the ID of the winner
                winner_id.append(winner_id_temp)
                winner_users.append(await ctx.bot.fetch_user(int(winner_id[i])))
                await ctx.send(f"Congrats on winning {winner_users[i].mention}!") #Send message pinging winner
                i+=1
        else:
            winner_id.append(str(voters[random.randint(0, len(voters) - 1)]))  # Get the ID of the winner
            winner_users.append(await ctx.bot.fetch_user(int(winner_id[i])))
            await ctx.send(f"Congrats on winning {winner_users[i].mention}!")  # Send message pinging winner


        #Edit original message so it's not still advertising a giveaway
        try:
            embed = discord.Embed(title=f"Giveaway ended!",description=f"Winner(s):\n")
            i = 0
            while i < numWinners:
                embed.add_field(name="~", value=f"Hosted by {ctx.message.author.mention}", inline=True)
                i+=1
            embed.add_field(name="Thank you to", value=f"{winner_users[i].mention}", inline=True)
            embed.set_footer(text='Giveaway ID: {}'.format(giveaway_message.id))
            await giveaway_message.edit(embed=embed)
        #Error if bot can't edit embed
        except discord.Forbidden:
            embed = discord.Embed(title="ERROR", description=f"Giveaway {id} was not hosted by {ctx.me.mention}. I cannot edit the embed")
            await user.send(embed=embed)


def setup(bot):
    bot.add_cog(Giveaway(bot))