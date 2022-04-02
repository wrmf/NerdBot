import discord
from discord.ext import commands
import random
import bot
from bot import *
from ids import *
from nukeIgnore import *
from permissions import *
import pandas as pd
import datetime


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
        @author Nerd#2022
        """

        # Check if user is none so bot doesn't crash
        if user is None:
            user = ctx.message.author
        if ctx.message.guild.id == 707226419993772112:
            LDLStaffDataframe = bot.getLdlStaff()

            columns = ["ID", "Name"]  # Columns for pandas array
            tempDataframe = pd.DataFrame({"ID": [user.id], "Name": [f"({user.name})"]})

            LDLStaffDataframe = pd.concat([LDLStaffDataframe, tempDataframe])
            LDLStaffDataframe.to_csv("ldl/ldl_staffText.csv", header=False, index=False)

            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**Success**", value=f"User {user.name} has been added as staff", inline=True)
            await ctx.send(embed=embed)




    @commands.command(aliases=['delLDLStaff'])
    @commands.check(is_admin)
    async def delLdlStaff(self, ctx: commands.Context, user: discord.Member = None):
        """
        Remove person from ignore list
        @author Nerd#2022
        """

        # Make sure user isn't none so the bot doesn't die
        if user is None:
            user = ctx.message.author

        if ctx.message.guild.id == 707226419993772112:
            LDLStaffDataframe = bot.getLdlStaff()


            LDLStaffDataframe.drop(LDLStaffDataframe["ID"].index(user.id))
            LDLStaffDataframe.to_csv("ldl/ldl_staffText.csv", header=False, index=False)

            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**Success**", value=f"User {user} has been removed from staff", inline=True)
            await ctx.send(embed=embed)


    @commands.command(aliases=['getLDLStaff'])
    @commands.check(is_admin)
    async def getLdlStaff(self, ctx: commands.Context):
        """
        Get the list of LDL staff
        @author @Nerd2021
        """

        # Read in CSV for LDL staff
        columns = ["ID", "Name"]  # Columns for pandas array
        LDLStaffDataframe = pd.read_csv("ldl/ldl_staffText.csv", header=None, delimiter="(", names=columns)
        LDLStaffDataframe["Name"] = LDLStaffDataframe["Name"].str[:-1]  # Delete ) from end of string
        LDLStaffDataframe.sort_values("Name")  # Sort values by code... does this do anything?

        embed = discord.Embed(color=ctx.author.color.value) #Create embed
        embed.add_field(name="Staff List", value=LDLStaffDataframe["Name"], inline=True) #Add ldl staff to embed
        embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
        await ctx.send(embed=embed) #Send embed

    @commands.command()
    @commands.check(is_mod)
    @commands.guild_only()
    async def addLOA(self, ctx: commands.Context, startDateStr: str, endDateStr: str):
        """
        Add LOA for LDL staff
        @param startDate: start date of LOA DD/MM/YYYY format
        @param endDate: start date of LOA DD/MM/YYYY format
        @author Nerd#2022
        """

        if ctx.message.guild.id != 707226419993772112:
            pass
        else:
            startDate = startDateStr.split("/")
            endDate = endDateStr.split("/")
            ldlLOADataframe = bot.getLOA()
            beginningDate = datetime.datetime(int(startDate[2]), int(startDate[1]), int(startDate[0]))
            endDate = datetime.datetime(int(endDate[2]), int(endDate[1]), int(endDate[0]))
            currentDate = datetime.datetime.today()

            if endDate > currentDate: #Make sure that end date is a future date
                columns = ["ID", "startDay", "startMonth", "startYear", "endDay", "endMonth", "endYear"]  # Columns for pandas array
                tempDataframe = pd.DataFrame({"ID":[ctx.message.author.id], "startDay":[startDate[0]],
                                                "startMonth":[startDate[1]], "startYear":[startDate[2]],
                                                "endDay":[endDate[0]], "endMonth":[endDate[1]], "endYear":[endDate[2]]})

                ldlLOADataframe = pd.concat([ldlLOADataframe, tempDataframe])

                ldlLOADataframe.to_csv("ldl/ldl_loa.csv", header=False, index=False)
                embed = discord.Embed(color=ctx.author.color.value)  # Create embed
                embed.add_field(name="LOA", value=f"Created LOA for user <@{ctx.message.author.id}> starting on "
                                                  f"{startDateStr} and ending on {endDateStr}", inline=True)  #Send confirmation message
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed
            else:
                embed = discord.Embed(color=ctx.author.color.value)  # Create embed
                embed.add_field(name="ERROR", value=f"You can't create an LOA with an end date in the past "
                                                    f"(though start dates in the past work fine)",inline=True)  #Create error embed
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed



def setup(bot):
    bot.add_cog(ldl(bot))