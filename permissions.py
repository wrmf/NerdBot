import discord
from discord.ext import commands

from nukeIgnore import *
import logging
import discord
from discord.ext import commands
import random
from ids import *

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


def is_plane(ctx: commands.Context):
    if ctx.author.id == TNMN or ctx.author.id == Likeusb:
        return True
    else:
        return False
def is_plane_or_admin(ctx: commands.Context):
    if is_plane(ctx) or is_admin(ctx):
        return True
    else:
        return False