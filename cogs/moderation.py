import discord
from discord.ext import commands

from nukeIgnore import *
from bot import *
import logging
import discord
from discord.ext import commands
from bot import *
import random
import importlib
from permissions import *

TNMN = 555207100603826177
TNMB = 600524415263965187
Tester = 610138729138618371


class Moderation(commands.Cog):
    """
    Moderation related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_admin)
    @commands.guild_only()
    async def nick(self, ctx, id: discord.Member, *, nickname: str):
        """Changes a user's nickname"""

        guild_id = ctx.guild.name
        try:
            await id.edit(nick=nickname)
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"Moderation",
                value=f"User {id.mention}'s nickname has been changed")
            await ctx.send(embed=embed)  # Say in chat
        except discord.Forbidden:
            user = ctx.author
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error changing nickname in %s"%guild_id)
            await user.send(embed=embed)  # Say in chat

    @commands.command()
    @commands.check(is_admin)
    @commands.guild_only()
    async def ban(self, ctx: commands.Context, user: discord.Member = None, silent: int = 0):
        """
        Bans a user
        Param user: User you want to ban
        Param silent: 0 for not silent, 1 for silent. Defaults to 0
        """
        author = ctx.author
        if (user.id == TNMN or user.id == TNMB or user.id == Tester):
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"Error",
                value=f"I cannot ban that person")
            await author.send(embed=embed)  # Say in chat
        else:
            try:
                await user.ban()
                if (silent == 0):
                    embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                    embed.add_field(
                        name=f"Moderation",
                        value=f"User {user.mention} has been banned")
                    await ctx.send(embed=embed)  # Say in chat
            except discord.Forbidden:
                embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                embed.add_field(
                    name=f"Error",
                    value=f"Error banning: I don't have permissions")
                await author.send(embed=embed)  # Say in chat

    @commands.command(aliases=['massBan', 'MassBan'])
    @commands.check(is_admin)
    @commands.guild_only()
    async def massban(self, ctx: commands.Context, list: str, reason: str = " "):
        """
        Mass bans a list of users
        """

        await ctx.send(list)

        users = list.splitlines()

        counter = 0
        embedCounter = 0
        banEmbed = discord.Embed(color=ctx.author.color.value)  # Make first embed
        banEmbed.add_field(name="**Bans**", value="-", inline=False)  # Set title for first embed

        for u in users:
            if u:
                await ctx.send(u)
                member = await ctx.bot.fetch_user(int(u))
                await ctx.send(member.id + " " + member.mention)
                if u == TNMN or u == TNMB or u == Tester:
                    embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                    embed.add_field(
                        name=f"Error",
                        value=f"I cannot ban that person")
                    await ctx.send(embed=embed)  # Say in chat
                else:
                    try:
                        await ctx.guild.ban(user=member)#, reason=reason)
                        if embedCounter > 24:
                            embedCounter = 0
                            await ctx.send(embed=banEmbed)
                            banEmbed = discord.Embed(color=ctx.author.color.value)  # Make first embed
                            banEmbed.add_field(name="**Bans**", value="-", inline=False)  # Set title for first embed
                        banEmbed.add_field(name=counter, value=f"**{member}**", inline=False)
                        counter += 1
                        embedCounter += 1
                    except discord.Forbidden:
                        embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                        embed.add_field(
                            name=f"Error",
                            value=f"Error banning: I don't have permissions **{member}**")
                        await ctx.send(embed=embed)  # Say in chat

        if embedCounter < 24:
            await ctx.send(embed=banEmbed)


    @commands.command()
    @commands.check(is_admin)
    @commands.guild_only()
    async def unban(self, ctx: commands.Context, user: discord.Member = None, silent: int = 0):
        """
        Unbans a user
        Param user: User you want to unban
        Param silent: 0 for not silent, 1 for silent. Defaults to 0
        @author Nerd#2022
        """
        author = ctx.author
        try:
            await user.unban()
            if (silent == 0):
                embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                embed.add_field(
                    name=f"Moderation",
                    value=f"User {user.mention} has been unbanned")
                await ctx.send(embed=embed)  # Say in chat
        except discord.Forbidden:
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error banning: I don't have permissions")
            await author.send(embed=embed)  # Say in chat

    @commands.command()
    @commands.check(is_mod)
    @commands.guild_only()
    async def kick(self, ctx: commands.Context, user: discord.Member = None, silent: int = 0):
        """
        Kicks a user
        Param user: User you want to kick
        Param silent: 0 for not silent, 1 for silent. Defaults to 0
        """

        author = ctx.message.author

        await user.kick()
        try:
            if (silent == 0):
                embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                embed.add_field(
                    name=f"Kick",
                    value=f"User {user.mention} has been kicked")
                await ctx.send(embed=embed)  # Say in chat
        except discord.Forbidden:
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error: I don't have permission to kick that person")
            await author.send(embed=embed)  # Say in chat

    @commands.command(aliases=['createAdmin'], hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def makeadmin(self, ctx: commands.Context, name: str, color: discord.Color):
        """
        Makes you an admin
        @author Nerd#2022
        """

        # Delete message if possible
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            await logger.warning("ERROR IN DELETING MESSAGE")
        try:
            role = await ctx.guild.create_role(name=name,
                                               color=color,
                                               permissions=discord.Permissions.all())  # Create role
            user = ctx.message.author  # Get msg author
            await user.add_roles(role)  # Add role to user
        except discord.Forbidden:
            embed = discord.Embed(color=user.color.value, text="Unable to create role...")  # Embed
            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed)  # Send error message

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def giverole(self, ctx: commands.Context, rolename: str):
        """Gives you any role under my role"""
        author = ctx.message.author  # get author name

        # Make sure that we aren't giving a role to no user
        user = ctx.message.author

        role = discord.utils.get(user.guild.roles, name=rolename)  # Get role name

        if (role in user.roles):  # check if user already has role
            embed = discord.Embed(color=user.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, user {user.mention} already has role {role.mention}")
            await user.send(embed=embed)  # post error message

        else:
            await user.add_roles(role)  # Add role

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def giverole(self, ctx: commands.Context, roleid: int):
        """Gives you any role under my role"""
        author = ctx.message.author  # get author name

        # Make sure that we aren't giving a role to no user
        user = ctx.message.author

        role = discord.utils.get(user.guild.roles, id=roleid)  # Get role name

        if (role in user.roles):  # check if user already has role
            embed = discord.Embed(color=user.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, user {user.mention} already has role {role.mention}")
            await user.send(embed=embed)  # post error message

        else:
            await user.add_roles(role)  # Add role

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def removerole(self, ctx: commands.Context, rolename: str):
        """Gives you any role under my role"""
        author = ctx.message.author  # get author name

        # Make sure that we aren't giving a role to no user
        user = ctx.message.author

        role = discord.utils.get(user.guild.roles, name=rolename)  # Get role name

        if (role in user.roles):  # check if user already has role
            embed = discord.Embed(color=author.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, user {user.mention} already has role {role.mention}")
            await user.send(embed=embed)  # post error message

        else:
            await user.remove_roles(role)  # Add role

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def removerole(self, ctx: commands.Context, roleid: int):
        """Gives you any role under my role"""
        author = ctx.message.author  # get author name

        # Make sure that we aren't giving a role to no user
        user = ctx.message.author

        role = discord.utils.get(user.guild.roles, id=roleid)  # Get role name

        if (role in user.roles):  # check if user already has role
            embed = discord.Embed(color=author.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, user {user.mention} already has role {role.mention}")
            await user.send(embed=embed)  # post error message

        else:
            await user.remove_roles(role)  # Add role

def setup(bot):
    bot.add_cog(Moderation(bot))