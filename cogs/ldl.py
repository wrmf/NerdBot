import discord
from discord.ext import commands
import random
import bot
from bot import *
from ids import *
from nukeIgnore import *
from permissions import *
import pandas as pd


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

        embed = discord.Embed(color=ctx.author.color.value)
        embed.add_field(name="**ERROR**", value="This command is deprecated, if you would like to add LDL staff, please contact Nerd#2022", inline=True)
        await ctx.send(embed=embed)

        # # Make sure person isn't trying to add themself or TNMN as staff
        # if (user.id == ctx.message.author.id or user.id == TNMN):
        #     embed = discord.Embed(color=ctx.author.color.value)
        #     embed.add_field(name="**ERROR**", value="You cannot add this person as staff!", inline=True)
        #     await ctx.send(embed=embed)
        #
        # elif (ctx.message.guild.id != LDL_server):
        #     embed = discord.Embed(color=ctx.author.color.value)
        #     embed.add_field(name="**ERROR**", value="You cannot add people as staff in a different server!", inline=True)
        #     await ctx.send(embed=embed)
        #
        # # Move onto adding the person
        # else:
        #     # Check if they are already staff
        #     if (user.id in ldl_staff[0]):
        #         embed = discord.Embed(color=ctx.author.color.value)
        #         embed.add_field(name="**ERROR**", value=f"User {user.mention} is already staff in the LDL server!",
        #                         inline=True)
        #         embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
        #         await ctx.send(embed=embed)
        #     # Add person to ignore list
        #     else:
        #         ldl_staffLocal = [ldl_staff[0], ldl_staff[1]]  # Duplicate list for saving to file purposes
        #
        #         ldl_staffLocal[0].append(user.id) #Add their ID
        #         ldl_staffLocal[1].append(user.display_name) #Add their display name
        #         # Fix the ldl_staff.py file
        #         with open("ldl_staff.py", 'r+') as file:
        #             file.truncate(0)
        #             string = "ldl_staff = [" + str(ldl_staffLocal[0]) + "," + str(ldl_staffLocal[1]) + "]"
        #             file.write(string)
        #             file.close()
        #         embed = discord.Embed(color=ctx.author.color.value) #Make embed
        #         embed.add_field(name="**Success**", value=f"User {user.mention} has been added as LDL server staff!",
        #                         inline=True) #Make sucess message
        #         embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
        #         await ctx.send(embed=embed) #Send embed


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

        embed = discord.Embed(color=ctx.author.color.value)
        embed.add_field(name="**ERROR**", value="This command is deprecated, if you would like to delete LDL staff, please contact Nerd#2022", inline=True)
        await ctx.send(embed=embed)

        # # Error if you are not in the LDL guild
        # if (ctx.guild.id != LDL_server):
        #     embed = discord.Embed(color=ctx.author.color.value) #Create embed
        #     embed.add_field(name="**ERROR**", value=f"You do cannot delete staff in another guild!", inline=True) #Add error to embed
        #     embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
        #     await ctx.send(embed=embed) #Sent error message
        # else:
        #     if (user.id in ldl_staff[0]):
        #
        #         ldl_staffLocal = [ldl_staff[0], ldl_staff[1]] #Create duplicate array
        #
        #         ldl_staffLocal[1].pop(ldl_staffLocal[0].index(user.id)) #Remove their display name
        #
        #         ldl_staffLocal[0].remove(user.id) #Remove ID
        #
        #         #Fix ldl_staff file
        #         with open("ldl_staff.py", 'r+') as file:
        #             file.truncate(0) #Empty the file
        #             string = "ldl_staff = [" + str(ldl_staffLocal[0]) + "," + str(ldl_staffLocal[1]) + "]" #Add the copy arrays
        #             file.write(string) #Write the files
        #             file.close() #Close file
        #
        #         embed = discord.Embed(color=ctx.author.color.value) #Make embed
        #         embed.add_field(name="**Success**", value=f"Deleted {user.mention} from staff list in LDL server",
        #                         inline=True) #Add success message
        #         embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
        #         await ctx.send(embed=embed) #Send embed
        #     else:
        #         embed = discord.Embed(color=ctx.author.color.value) #Make embed
        #         embed.add_field(name="**ERROR**", value=f"User {user.mention} is not staff in the LDL server", inline=True) #Error message
        #         embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
        #         await ctx.send(embed=embed) #Send embed


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

            columns = ["ID", "startDay", "startMonth", "startYear", "endDay", "endMonth", "endYear"]  # Columns for pandas array
            tempDataframe = pd.DataFrame({"ID":[ctx.message.author.id], "startDay":[startDate[0]],
                                            "startMonth":[startDate[1]], "startYear":[startDate[2]],
                                            "endDay":[endDate[0]], "endMonth":[endDate[1]], "endYear":[endDate[2]]})

            await ctx.send("got here")

            ldlLOADataframe = pd.concat([ldlLOADataframe, tempDataframe])

            ldlLOADataframe.to_csv("ldl/ldl_loa.csv", header=False)

            await ctx.send(ldlLOADataframe)

            embed = discord.Embed(color=ctx.author.color.value)  # Create embed
            embed.add_field(name="LOA", value=f"Created LOA for user <@{ctx.message.author.id}> starting on "
                                              f"{startDateStr} and ending on {endDateStr}", inline=True)  # Add ldl staff to embed
            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(ldl(bot))