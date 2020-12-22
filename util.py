import discord.ext.commands


def is_admin(ctx: discord.ext.commands.Context):
    return ctx.author.id == 588082004545896452
