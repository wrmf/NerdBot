import discord
from discord.ext import commands
import random

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, question: str, *options: str):
        """
        Creates a poll.
        """
        if (is_LDL_channel(ctx)):
            if len(options) <= 1:
                await ctx.send('You cannot make a poll out of 1 item!')
                return
            if len(options) > 10:
                await ctx.send('You cannot make a poll for more than 10 things!')
                return

            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

            description = []
            for x, option in enumerate(options):
                description += '\n {} {}'.format(reactions[x], option)
            embed = discord.Embed(title=question, description=''.join(description))
            react_message = await ctx.send(embed=embed)
            for reaction in reactions[:len(options)]:
                await react_message.add_reaction(reaction)
            embed.set_footer(text='Poll ID: {}'.format(react_message.id))
            await react_message.edit(embed=embed)

    @commands.command(pass_context=True)
    async def tally(self, ctx: commands.Context, id):
        """
        Tally poll.
        """
        if (is_LDL_channel(ctx)):
            poll_message = await ctx.fetch_message(id)
            if not poll_message.embeds:
                return
            embed = poll_message.embeds[0]
            if poll_message.author != ctx.me:
                return
            if not embed.footer.text.startswith('Poll ID:'):
                return
            unformatted_options = [x.strip() for x in embed.description.split('\n')]
            opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
                else {x[:1]: x[2:] for x in unformatted_options}
            # check if we're using numbers for the poll, or x/checkmark, parse accordingly
            voters = [ctx.me.id]  # add the bot's ID to the list of voters to exclude it's votes

            tally = {x: 0 for x in opt_dict.keys()}
            for reaction in poll_message.reactions:
                if reaction.emoji in opt_dict.keys():
                    reactors = await reaction.users().flatten()
                    for reactor in reactors:
                        if reactor.id not in voters:
                            tally[reaction.emoji] += 1
                            voters.append(reactor.id)

            output = 'Results of the poll for "{}":\n'.format(embed.title) + \
                     '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
            await ctx.send(output)

def setup(bot):
    bot.add_cog(Poll(bot))

