import discord
from discord.ext import commands
import random
from bot import *
from ids import *
from nukeIgnore import *
from permissions import *


class ldl(commands.Cog):
    """
    Nuke related commandss
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addLDLStaff'])
    @commands.check(is_admin)
    async def addLdlStaff(self, ctx: commands.Context, user: discord.Member = None):
        """
        Add person as staff on LDL server
        @author Nerd#2021
        """

        # Check if user is none so bot doesn't crash
        if user is None:
            user = ctx.message.author

        # Make sure person isn't trying to add themself or TNMN as staff
        if (user.id == ctx.message.author.id or user.id == TNMN):
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You cannot add this person as staff!", inline=True)
            await ctx.send(embed=embed)

        elif (ctx.message.guild.id != LDL_server):
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You cannot add people as staff in a different server!", inline=True)
            await ctx.send(embed=embed)

        # Move onto adding the person
        else:
            # Check if they are already staff
            if (user.id in ldl_staff[0]):
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"User {user.mention} is already staff in the LDL server!",
                                inline=True)
                await ctx.send(embed=embed)
            # Add person to ignore list
            else:
                ldl_staffLocal = [ldl_staff[0], ldl_staff[1]]  # Duplicate list for saving to file purposes

                ldl_staffLocal[0].append(user.id) #Add their ID
                ldl_staffLocal[1].append(user.display_name) #Add their display name
                # Fix the ldl_staff.py file
                with open("ldl_staff.py", 'r+') as file:
                    file.truncate(0)
                    string = "ldl_staff = [" + str(ldl_staffLocal[0]) + "," + str(ldl_staffLocal[1]) + "]"
                    file.write(string)
                    file.close()
                embed = discord.Embed(color=ctx.author.color.value) #Make embed
                embed.add_field(name="**Success**", value=f"User {user.mention} has been added as LDL server staff!",
                                inline=True) #Make sucess message
                await ctx.send(embed=embed) #Send embed


    @commands.command(aliases=['delLDLStaff'])
    @commands.check(is_admin)
    async def delLdlStaff(self, ctx: commands.Context, user: discord.Member = None):
        """
        Remove person from ignore list
        @author Nerd#2021
        """

        # Make sure user isn't none so the bot doesn't die
        if user is None:
            user = ctx.message.author

        # Error if you are not in the LDL guild
        if (ctx.guild.id != LDL_server):
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value=f"You do cannot delete staff in another guild!", inline=True)
            await ctx.send(embed=embed)
        else:
            if (user.id in ldl_staff[0]):

                ldl_staffLocal = [ldl_staff[0], ldl_staff[1]]

                ldl_staffLocal[1].pop(ldl_staffLocal[0].index(user.id))

                ldl_staffLocal[0].remove(user.id)

                with open("ldl_staff.py", 'r+') as file:
                    file.truncate(0)
                    string = "ldl_staff = [" + str(ldl_staffLocal[0]) + "," + str(ldl_staffLocal[1]) + "]"
                    file.write(string)
                    file.close()

                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**Success**", value=f"Deleted {user.mention} from staff list in LDL server",
                                inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"User {user.mention} is not staff in the LDL server", inline=True)
                await ctx.send(embed=embed)


    @commands.command(aliases=['getLDLStaff'])
    @commands.check(is_admin)
    async def getLdlStaff(self, ctx: commands.Context):
        """
        Get the list of LDL staff
        @author @Nerd2021
        """

        embed = discord.Embed(color=ctx.author.color.value)
        embed.add_field(name="Staff List", value=ldl_staff[1], inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ldl(bot))