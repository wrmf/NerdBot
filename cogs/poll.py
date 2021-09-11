import discord
from discord.ext import commands
import random
from bot import *
from permissions import *


class Poll(commands.Cog):
    """
    Poll related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, question: str, *options: str):
        """
        Creates a poll.
        @author Paladin Of Ioun#5905
        @author Nerd#2021
        """

        #Check if channel is an LDL channel
        if (is_LDL_channel(ctx)):
            if len(options) <= 1:
                await ctx.send('You cannot make a poll out of 1 item!')
                return
            if len(options) > 10:
                await ctx.send('You cannot make a poll for more than 10 things!')
                return

            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟'] #Set reactinos for poll

            description = []
            for x, option in enumerate(options):
                description += '\n {} {}'.format(reactions[x], option)
            embed = discord.Embed(title=question, description=''.join(description)) #Create embed
            react_message = await ctx.send(embed=embed) #Send embed
            for reaction in reactions[:len(options)]:
                await react_message.add_reaction(reaction) #Add reactions from above
            embed.set_footer(text='Poll ID: {}'.format(react_message.id)) #Add poll id (message.id)
            await react_message.edit(embed=embed) #Edit message for ID

    @commands.command(pass_context=True)
    async def tally(self, ctx: commands.Context, id):
        """
        Tally poll
        @author Paladin Of Ioun#5905
        @author Nerd#2021
        """

        #Check if channel is an LDL channel
        if (is_LDL_channel(ctx)):
            poll_message = await ctx.fetch_message(id)

            #Check if poll has an embed
            if not poll_message.embeds:
                return

            embed = poll_message.embeds[0] #Set embed

            #Don't tally poll if poll is not made by you
            if poll_message.author != ctx.me or poll_message.author != TNMN:
                return

            #Make sure that poll has a poll ID attached to it
            if not embed.footer.text.startswith('Poll ID:'):
                return
            unformatted_options = [x.strip() for x in embed.description.split('\n')] #Set unformatted options
            opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
                else {x[:1]: x[2:] for x in unformatted_options}
            # check if we're using numbers for the poll, or x/checkmark, parse accordingly

            voters = [ctx.me.id]  # add the bot's ID to the list of voters to exclude it's votes

            tally = {x: 0 for x in opt_dict.keys()} #Tally all of the votes
            for reaction in poll_message.reactions:
                if reaction.emoji in opt_dict.keys():
                    reactors = await reaction.users().flatten()
                    for reactor in reactors:
                        if reactor.id not in voters:
                            tally[reaction.emoji] += 1
                            voters.append(reactor.id)

            output = 'Results of the poll for "{}":\n'.format(embed.title) + \
                     '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()]) #Generate results embed

            await ctx.send(output)
            embed = discord.Embed(color=ctx.author.color.value, text=output)  # Create embed
            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed)  # Sent error message


def setup(bot):
    bot.add_cog(Poll(bot))

