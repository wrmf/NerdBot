from io import BytesIO
import logging
import os

import discord
import random
from discord.ext import commands
import youtube_dl
import ffmpeg

########
#People#
########

TNMN = 555207100603826177
Paladin = 447068325856542721
Cadence = 363424348742352906
Macky = 523919572273856523
TNMB = 600524415263965187

teen_club = 609496545569800192
programmer_club = 555087033652215830

logger = logging.getLogger("bot")

def fmt(d):
    return d.strftime('%A, %B %e %Y at %H:%M:%S')

def is_nuke(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles
    return is_mod(ctx) or is_admin(ctx) or is_owner(ctx)

def is_owner(ctx: commands.Context):
    return ctx.author.id == 555207100603826177


def is_admin(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles
    return is_owner(ctx) or any([role.permissions.administrator for role in roles])


def is_mod(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles
    return is_admin(ctx) or any([role.permissions.manage_messages for role in roles])

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Discord_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def pfp(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        if user is None:
            user = ctx.author

        await ctx.send(f"{user.avatar_url_as(size=1024)}")

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        """ Get all roles in current server """
        allroles = ""

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
        #Final version by Nerd#8909

        if user is None:
            user = ctx.author

        io = False

        if user.id == ctx.guild.owner.id:
            io = True

        embed = discord.Embed(color=user.color.value)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="Name", value=user, inline=True)
        embed.add_field(name="Nickname", value=user.nick if hasattr(user, "nick") else "None", inline=True)
        embed.add_field(name="Account created", value=fmt(user.created_at), inline=True)
        embed.add_field(name=f"Joined {ctx.guild.name}", value=fmt(user.joined_at), inline=True)
        embed.add_field(name="Is owner:", value=io, inline = True)

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
        if i is not 1:
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

class moderation(commands.Cog):
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
        if (user.id == TNMN == TNMB):
            embed = discord.Embed(color=ctx.message.author.top_role.color.value)
            embed.add_field(
                name=f"Error",
                value=f"I cannot ban that person")
            await author.send(embed=embed)  # Say in chat
        else:
            try:
                await user.ban()
                if(silent == 0):
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
            if (silent is 0):
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

class Locked(commands.Cog):
    """ 
    Locked down commands (only a few people can use)
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def logout(self, ctx: commands.Context):
        """Quits bot."""
        embed = discord.Embed(color=ctx.message.author.top_role.color.value)
        embed.add_field(
            name=f"Command",
            value=f"Logging out")
        await ctx.send(embed=embed)  # Say in chat
        await self.bot.logout()
        await self.bot.close()
        exit(0)

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
    async def ma(self, ctx: commands.Context, name: str, color: discord.Color):
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
    async def gr(self, ctx: commands.Context, rolename: str):
        """Gives you any role under my role"""
        author = ctx.message.author #get author name

        #Make sure that we aren't giving a role to no user
        user = ctx.message.author

        role = discord.utils.get(user.guild.roles, name=rolename) #Get role name

        if(role in user.roles): #check if user already has role
            embed = discord.Embed(color=user.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, user {user.mention} already has role {role.mention}")
            await user.send(embed=embed) #post error message

        else:
            await user.add_roles(role) #Add role

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def rr(self, ctx: commands.Context, rolename: str):
        """Gives you any role under my role"""
        author = ctx.message.author #get author name

        #Make sure that we aren't giving a role to no user
        user = ctx.message.author

        role = discord.utils.get(user.guild.roles, name=rolename) #Get role name

        if(role in user.roles): #check if user already has role
            embed = discord.Embed(color=author.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, user {user.mention} already has role {role.mention}")
            await user.send(embed=embed) #post error message

        else:
            await user.remove_roles(role) #Add role


class Useful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, question: str, *options: str):
        """
        Creates a poll.
        """

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

class Voice(commands.Cog):
    """
    Talking commands that aren't particularly useful
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Joins voice channel"""
        if hasattr(ctx.message.author.voice, 'channel'):
            channel = ctx.message.author.voice.channel
            user = ctx.message.author

            await channel.connect()
            embed = discord.Embed(color=user.color.value)
            embed.add_field(
                name=f"Music",
                value=f"Joined channel")
            await ctx.send(embed=embed)  # Say in chat
        else:
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error: you are not in a voice channel")
            await ctx.send(embed=embed) #Say in chat

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx):
        """Leaves voice channel"""
        server = ctx.message.guild.voice_client
        """Leaves voice channel"""
        if hasattr(ctx.message.author.voice, 'channel'):
            channel = ctx.message.author.voice.channel
            user = ctx.message.author

            await server.disconnect()
            embed = discord.Embed(color=user.color.value)
            embed.add_field(
                name=f"Music",
                value=f"Left channel")
            await ctx.send(embed=embed)  # Say in chat
        else:
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error: I am not in a voice channel")
            await ctx.send(embed=embed)  # Say in chat

    @commands.command()
    @commands.check(is_admin)
    async def dj(self, ctx: commands.Context, *, user: discord.Member = None):
        """Gives you DJ role (able to control music)"""
        author = ctx.message.author #get author name

        #Make sure that we aren't giving a role to no user
        if user is None:
            user = ctx.message.author

        if not hasattr(user.guild.roles, 'dj'):
            role2 = await ctx.guild.create_role(name='DJ')
            embed = discord.Embed(color=author.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, {ctx.guild.name} has no role {role2.name}. Creating!")
            await ctx.send(embed=embed) #post error message

        role = discord.utils.get(user.guild.roles, name='DJ')  # Get role name

        if(role in user.roles): #check if user already has role
            embed = discord.Embed(color=author.color.value)
            embed.add_field(
                name=f"Error",
                value=f"Error, user {user.mention} already has role {role.mention}")
            await ctx.send(embed=embed) #post error message

        else:
            await user.add_roles(role) #Add role

            embed = discord.Embed(color=author.color.value)
            embed.add_field(
                name=f"Role Given",
                value=f"User {user.mention} has been given {role.mention} role by {author.mention}")
            await ctx.send(embed=embed) #Say in chat

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.check(is_owner)
    async def echo(self, ctx, num: int, ste: str):
        i = 0
        await ctx.channel.purge(limit=1)
        while(i < num):
            await ctx.send(ste)
            i = i+1



def setup(bot):
    bot.add_cog(Discord_Info(bot))
    bot.add_cog(moderation(bot))
    bot.add_cog(Locked(bot))
    bot.add_cog(Useful(bot))
    bot.add_cog(Voice(bot))




