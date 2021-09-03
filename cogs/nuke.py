import discord
from discord.ext import commands
import random
from bot import *
from ids import *
from nukeIgnore import *

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


class Nuke(commands.Cog):
    """
    Nuke related commandss
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_nuke)
    async def nuke(self, ctx: commands.Context, limit: int):
        """ Nuke a large number of messages """
        # Concept by Paladin Of Ioun#5905
        # Final version by Nerd#2021
        if ctx.message.author.id in nukeArray[0] and "ALL" == nukeArray[1][nukeArray[0].index(ctx.message.author.id)]:
            await ctx.send(f"You have been disallowed from using nuke ALL guilds")
        elif ctx.message.author.id in nukeArray[0] and ctx.message.guild.id == nukeArray[1][nukeArray[0].index(ctx.message.author.id)]:
            await ctx.send(f"You have been disallowed from using nuke in guild {nukeArray[1][nukeArray[0].index(ctx.message.author.id)]}")
        else:
            """Nuke messages"""
            try:
                await ctx.channel.purge(limit=limit+1)
            except discord.Forbidden:
                embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                embed.add_field(
                    name=f"Error",
                    value=f"Error: I don't have permission to nuke")
                await ctx.send(embed=embed)  # Say in chat

    @commands.command()
    @commands.check(is_admin)
    ##################################
    #Add a person to nuke ignore list#
    ##################################
    async def addNukeIgnore(self, ctx: commands.Context, user: discord.Member = None, guild: str = None):
        """ Add person to nuke ignore list """
        # Written by Nerd#2021

        #Check if user is none so bot doesn't crash
        if user is None:
            user = ctx.message.author

        #Check if guild is none so bot doesn't crash
        if guild is None:
            guild = ctx.guild.id

        #Make sure person isn't trying to ignore themself or TNMN
        if(user.id == ctx.message.author.id or user.id == TNMN):
            await ctx.send("You cannot nuke ignore this person from nuke")
        #Make sure person has permission to ignore in the guild they are trying to ignore in
        elif(guild != ctx.guild.id and ctx.message.author.id != TNMN):
            await ctx.send("You do not have permission to ignore this person in that guild")
        #Move onto ignoring the person
        else:
            nukeArrayLocal = [nukeArray[0], nukeArray[1]] #Duplicate list for saving to file purposes
            #Check if they are already ignored
            if(user.id in nukeArray[0] and
                    nukeArray[1][nukeArray[0].index(user.id)] == guild):
                await ctx.send(f"User {user.mention} is already nuke ignored in server {nukeArrayLocal[1][nukeArrayLocal[0].index(user.id)]}")
            #Add person to ignore list
            else:
                nukeArrayLocal[0].append(user.id)
                nukeArrayLocal[1].append(guild)
                #Fix the nukeIgnore.py file
                with open("nukeIgnore.py", 'r+') as file:
                    file.truncate(0)
                    string = "nukeArray = [" +str(nukeArrayLocal[0])+"," +str(nukeArrayLocal[1])+"]"
                    file.write(string)
                    file.close()
                if(guild == "ALL"):
                    await ctx.send(f"Added user {user.mention} to nuke ignore in ALL guilds")
                else:
                    await ctx.send(f"Added user {user.mention} to nuke ignore in guild **{ctx.guild}**")

    @commands.command()
    @commands.check(is_admin)
    async def delNukeIgnore(self, ctx: commands.Context, user: discord.Member = None, guild: str = None):
        """ Remove person from ignore list """
        #Make sure user isn't none so the bot doesn't die
        if user is None:
            user = ctx.message.author
        #Make sure guild isn't none so bot doesn't die

        if guild is None:
            guild = ctx.guild.id

        if(guild != ctx.guild.id and ctx.message.author.id != TNMN):
            await ctx.send("You do not have permission to unignore this person in that guild")
        else:
            nukeArrayLocal2 = [nukeArray[0], nukeArray[1]]
            if(user.id in nukeArray[0] and
                    nukeArray[1][nukeArray[0].index(user.id)] == guild):
                nukeArrayLocal2[1].pop(nukeArrayLocal2[0].index(user.id))

                nukeArrayLocal2[0].remove(user.id)
                with open("nukeIgnore.py", 'r+') as file:
                    file.truncate(0)
                    string = "nukeArray = [" +str(nukeArrayLocal2[0])+"," +str(nukeArrayLocal2[1])+"]"
                    file.write(string)
                    file.close()

                await ctx.send(f"Added user {user.mention} to nuke ignore in guild **{ctx.guild}**")
            else:
                await ctx.send(f"User {user.mention} is already nuke unignored in that server")

def setup(bot):
    bot.add_cog(Nuke(bot))