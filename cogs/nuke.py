import discord
from discord.ext import commands
import random
from bot import *
from ids import *
from nukeIgnore import *
from permissions import *


class Nuke(commands.Cog):
    """
    Nuke related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_nuke)
    async def nuke(self, ctx: commands.Context, limit: int):
        """
        Nuke a large number of messages
        @author Paladin Of Ioun #5905
        @author Nerd#2021
        """

        #Check if the user is nuke ignored
        if ctx.message.author.id in nukeArray[0] and "ALL" == nukeArray[1][nukeArray[0].index(ctx.message.author.id)]:
            await ctx.send(f"You have been disallowed from using nuke ALL guilds")
        elif ctx.message.author.id in nukeArray[0] and ctx.message.guild.id == nukeArray[1][nukeArray[0].index(ctx.message.author.id)]:
            await ctx.send(f"You have been disallowed from using nuke in guild {nukeArray[1][nukeArray[0].index(ctx.message.author.id)]}")
        else:
            #nuke messages
            try:
                await ctx.channel.purge(limit=limit+1) #Actually nuke
            #error in case bot doesn't have permission
            except discord.Forbidden:
                embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                embed.add_field(
                    name=f"Error",
                    value=f"Error: I don't have permission to nuke")
                await ctx.send(embed=embed)  # Say in chat

    @commands.command()
    @commands.check(is_admin)
    async def addNukeIgnore(self, ctx: commands.Context, user: discord.Member = None, guild: str = None):
        """
        Add a person to the Nuke ignore list
        @author Nerd#2021
        """

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
        """
        Remove person from nuke ignore list
        @author Nerd#2021
        """
        #Make sure user isn't none so the bot doesn't die
        if user is None:
            user = ctx.message.author

        #Make sure guild isn't none so bot doesn't die
        if guild is None:
            guild = ctx.guild.id

        #Check if person has permission to use this command
        if(guild != ctx.guild.id and ctx.message.author.id != TNMN):
            await ctx.send("You do not have permission to unignore this person in that guild")
        #Delete person from nukeIgnore
        else:
            nukeArrayLocal2 = [nukeArray[0], nukeArray[1]] #Create a temp copy
            if(user.id in nukeArray[0] and
                    nukeArray[1][nukeArray[0].index(user.id)] == guild):
                nukeArrayLocal2[1].pop(nukeArrayLocal2[0].index(user.id)) #Remove guild ID

                nukeArrayLocal2[0].remove(user.id) #Remove person ID

                #fix nukeIgnore file
                with open("nukeIgnore.py", 'r+') as file:
                    file.truncate(0)
                    string = "nukeArray = [" +str(nukeArrayLocal2[0])+"," +str(nukeArrayLocal2[1])+"]"
                    file.write(string)
                    file.close()

                await ctx.send(f"Removed user {user.mention} from nuke ignore in guild **{ctx.guild}**") #Confirmation of removal
            else:
                await ctx.send(f"User {user.mention} is already nuke unignored in that server") #Error

def setup(bot):
    bot.add_cog(Nuke(bot))