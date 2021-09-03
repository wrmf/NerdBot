import discord
from discord.ext import commands
from permChecks import *
import random

logger = logging.getLogger("bot")

import logging
import discord
from discord.ext import commands
from bot import *
import random

logger = logging.getLogger("bot")

def fmt(d):
    return d.strftime('%A, %B %e %Y at %H:%M:%S')

def is_nuke(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles

    return is_mod(ctx) or is_admin(ctx) or is_owner(ctx)

def is_owner(ctx: commands.Context):
    return ctx.author.id == TNMN


def is_admin(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles
    return is_owner(ctx) or any([role.permissions.administrator for role in roles])


def is_mod(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles
    return is_admin(ctx) or any([role.permissions.manage_messages for role in roles])

def is_LDL_channel(ctx: commands.Context):
    if(ctx.guild.id == LDL_server):
        if(ctx.message.channel.id == LDL_bot_commands or ctx.message.channel.id == LDL_bot_test):
            return True
        else:
            return False
    else:
        return True

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
    if (is_LDL_channel(ctx)):
        #reaction = '🎉'
        reaction = '<:celebrate_animated:883452218840334346>'

        embed = discord.Embed(title="Giveaway!", description=item)
        react_message = await ctx.send(embed=embed)
        await react_message.add_reaction(reaction)
        embed.set_footer(text='Giveaway ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)


    @commands.command(pass_context=True)
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
        voters.remove(giveaway_message.author.id)
        if (len(voters) <= 0):
            embed = discord.Embed(title="ERROR", description="No one has entered this giveaway!",
                                  color=ctx.message.author.top_role.color)
            await ctx.send(embed=embed)
            return
        winner_id = str(voters[random.randint(0, len(voters) - 1)])
        await ctx.send("Congrats on winning <@" + winner_id + ">!")
        embed = discord.Embed(title="Giveaway!", description="Winner: <@" + winner_id + ">!")
        embed.set_footer(text='Giveaway ID: {}'.format(giveaway_message.id))
        await giveaway_message.edit(embed=embed)