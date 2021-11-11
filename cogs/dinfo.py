import discord
from discord.ext import commands

from nukeIgnore import *
from bot import *
import logging
import discord
from discord.ext import commands
from bot import *
import random
from permissions import *



class Discord_Info(commands.Cog):
    """
    Discord info commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def getGuilds(self, ctx):
        """
        Get the list of guilds that the bot is in
        @author Nerd#2021
        """

        embed = discord.Embed(color=ctx.author.color.value) #Create embed
        embed.add_field(name="**Guilds**", value="-", inline=True) #Add title
        counter = 0 #Set a counter for the number of guilds to 0

        #Add guilds to embed
        async for guild in client.fetch_guilds(limit=200):
            counter = counter+1
            embed.add_field(name=counter, value=guild.name, inline=True)

        embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
        await ctx.send(embed=embed) #Send embed

    @commands.command()
    @commands.guild_only()
    async def pfp(self, ctx, *, user: discord.Member = None):
        """
        Get the avatar of you or someone else
        @author Paladin Of Ioun#5905
        @author Nerd#2021
        """

        #Make sure bot doesn't crash if user doesn't exist
        if user is None:
            user = ctx.author

        #Sent profile photo
        if(is_LDL_channel(ctx)):
            await ctx.send(f"{user.avatar_url_as(size=2048)}")  # Send message

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        """
        Get all roles in current server
        @author Nerd#2021
        """

        allroles = "" #Make an empty string with roles

        if (is_LDL_channel(ctx)):
            author = ctx.author #Set author

            embed = discord.Embed(color=author.color.value) #Create embed

            roles = ctx.guild.roles #Get guild roles
            roles.reverse() #Reverse the roles list (they come out in backwards order)

            embed.add_field(
                name=f"Roles for {ctx.guild.name}",
                value=', '.join([f"<@&{x.id}>" for x in roles if x is not ctx.guild.default_role
                                 ]) if len(ctx.guild.roles) > 1 else f"No roles in {ctx.guild.name}",
                inline=False
            ) #Add roles to embed

            embed.set_footer(text=f"Message requested by {author}") #Footer

            await ctx.send(embed=embed) #Send embed

    @commands.command()
    @commands.guild_only()
    async def user(self, ctx, *, user: discord.Member = None):
        """
        Get user information
        @author Paladin Of Ioun#5905
        @author Nerd#2021
        """

        #Make sure user isn't none
        if user is None:
            user = ctx.author

        if (is_LDL_channel(ctx)):

            embed = discord.Embed(color=user.color.value) #Create embed
            embed.set_thumbnail(url=user.avatar_url) #Create embed thumbnail

            embed.add_field(name="Name", value=user, inline=True) #Add name field
            embed.add_field(name="Nickname", value=user.nick if hasattr(user, "nick") else "None", inline=True) #Add nickname field
            embed.add_field(name="Account created", value=fmt(user.created_at), inline=True) #Add when their account was created
            embed.add_field(name=f"Joined {ctx.guild.name}", value=fmt(user.joined_at), inline=True) #Add when their account joined this server

            roles = user.roles #Get roles that the user has
            roles.reverse() #Reverse roles

            embed.add_field(
                name="Roles",
                value=', '.join([f"<@&{x.id}>" for x in roles if x is not ctx.guild.default_role]) if len(user.roles) > 1 else f"No roles in {ctx.guild.name}",
                inline=False
            ) #Add their roles to the embed

            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed) #Send embed

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, role: discord.Role):
        """
        Get role information
        @author Nerd#2021
        """

        # Make sure user isn't none
        if role is None or ctx.guild.get_role(role.id) is None:
            embed.add_field(name="**ERROR**", value="Invalid role", inline=True) #Set title for first embed
            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed)  # Send embed

        if (is_LDL_channel(ctx)):
            embed = discord.Embed(color=role.color.value) #Create embed

            embed.add_field(name="Name", value=role.name, inline=False)  # Add name field
            embed.add_field(name="ID", value=role.id, inline=False)  # Add name field
            embed.add_field(name="Color", value=role.color.value, inline=False)  # Add color field
            embed.add_field(name="Permissions info", value=role.permissions, inline=False) #Add permissions field
            embed.add_field(name="Created at", value=role.created_at, inline=False)  # Add permissions field


            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed)  # Send embed

    @commands.group()
    @commands.guild_only()
    async def server(self, ctx):
        """
        Check info about current server
        @author Paladin Of Ioun#5905
        @author Nerd#2021
        """
        if (is_LDL_channel(ctx)):
            if ctx.invoked_subcommand is None:
                findbots = sum(1 for member in ctx.guild.members if member.bot) #Find the number of bots in the guild

                allroles = "" #Roll list

                #Find all of the roles
                for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
                    allroles += f"{role.name}\n"

                author = ctx.message.author #Get author

                embed = discord.Embed(color=author.top_role.color.value) #Create embed
                embed.set_thumbnail(url=ctx.guild.icon_url) #Set embed thumbnail
                embed.add_field(name="Server Name", value=ctx.guild.name, inline=True) #Add server name to embed
                embed.add_field(name="Server ID", value=ctx.guild.id, inline=True) #Add server ID to embed
                embed.add_field(name="Members", value=ctx.guild.member_count, inline=True) #Add member count to embed
                embed.add_field(name="Bots", value=str(findbots), inline=True) #Add bots count to embed
                embed.add_field(name="Owner", value=ctx.guild.owner, inline=True) #Add guild owner to embed ***BROKEN SINCE 2020***
                embed.add_field(name="Created", value=fmt(ctx.guild.created_at), inline=True) #Add when the guild was created to embed

                roles = ctx.guild.roles #Get roles
                roles.reverse() #Reverse the roles

                embed.add_field(
                    name="Roles",
                    value=', '.join([f"<@&{x.id}>" for x in roles if x is not ctx.guild.default_role]) if len(
                        ctx.guild.roles) > 1 else f"No roles in {ctx.guild.name}",
                    inline=False
                ) #Add roles to embed

                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed) #Send embed

    @commands.command()
    @commands.guild_only()
    async def emoji(self, ctx):
        """
        Get all emojis in a server
        @author Nerd#2021
        """

        if (is_LDL_channel(ctx)):

            embed = discord.Embed(color=ctx.author.color.value) #Make first embed
            embed.add_field(name="**Emojis**", value="-", inline=True) #Set title for first embed

            embed2 = discord.Embed(color=ctx.author.color.value) #Make second embed
            embed2.add_field(name="**Emojis**", value="-", inline=True) #Set title for second embed

            embed3 = discord.Embed(color=ctx.author.color.value) #Make third embed
            embed3.add_field(name="**Emojis**", value="-", inline=True) #Set title for third embed

            i = 1 #Make emoji counter


            for x in ctx.guild.emojis:
                #Make sure we aren't adding emotes to a full embed
                if(i<=24):
                    embed.add_field(name=i, value=x, inline=True)
                elif(i<=48):
                    embed2.add_field(name=i, value=x, inline=True)
                else:
                    embed3.add_field(name=i, value=x, inline=True)
                i = i+1

            #Sent messages that are full (don't send empty ones)
            if i != 1:
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed = embed)

                if(i > 25):
                    embed2.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                    await ctx.send(embed = embed2)

                if (i > 49):
                    embed3.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                    await ctx.send(embed=embed3)
            #Send error message if there are no emotes
            else:
                embed4 = discord.Embed(color=ctx.author.color.value)
                embed4.add_field(name="**Emojis**", value=f"No emojis found for  **{ctx.guild.name}**", inline=True)
                embed4.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed4) #Send embed

def setup(bot):
    bot.add_cog(Discord_Info(bot))




