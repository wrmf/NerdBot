import logging
import discord
from discord.ext import commands

from nukeIgnore import *
from ids import *
from ldl_staff import *
from bot import *
print("IMPORTED")

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

class Discord_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_owner)
    async def getGuilds(self, ctx):
        """Get the list of guilds that the bot is in"""
        embed = discord.Embed(color=ctx.author.color.value)
        embed.add_field(name="**Guilds**", value="-", inline=True)
        i = 0
        async for guild in client.fetch_guilds(limit=200):
            i = i+1
            embed.add_field(name=i, value=guild.name, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def pfp(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        if user is None:
            user = ctx.author
        if(is_LDL_channel(ctx)):
            await ctx.send(f"{user.avatar_url_as(size=2048)}")

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
        """ Nuke a large number of messages """
        # Concept by Paladin Of Ioun#5905
        # Final version by Nerd#2021
        if ctx.message.author.id in nukeArray[0] and "ALL" == nukeArray[1][nukeArray[0].index(ctx.message.author.id)]:
            await ctx.send(f"You have been disallowed from using nuke ALL guilds")
        elif ctx.message.author.id in nukeArray[0] and ctx.message.guild.id == nukeArray[1][nukeArray[0].index(ctx.message.author.id)]:
            await ctx.send(f"You have been disallowed from using nuke in guild {nukeArray[1][nukeArray[0].index(ctx.message.author.id)]}")
        else:
            """Nuke messages"""
            try:
                await ctx.channel.purge(limit=limit+1)
            except discord.Forbidden:
                embed = discord.Embed(color=ctx.message.author.top_role.color.value)
                embed.add_field(
                    name=f"Error",
                    value=f"Error: I don't have permission to nuke")
                await ctx.send(embed=embed)  # Say in chat

    @commands.command()
    @commands.check(is_admin)
    ##################################
    #Add a person to nuke ignore list#
    ##################################
    async def addNukeIgnore(self, ctx: commands.Context, user: discord.Member = None, guild: str = None):
        """ Add person to nuke ignore list """
        # Written by Nerd#2021

        #Check if user is none so bot doesn't crash
        if user is None:
            user = ctx.message.author

        #Check if guild is none so bot doesn't crash
        if guild is None:
            guild = ctx.guild.id

        #Make sure person isn't trying to ignore themself or TNMN
        if(user.id == ctx.message.author.id or user.id == TNMN):
            await ctx.send("You cannot nuke ignore this person from nuke")
        #Make sure person has permission to ignore in the guild they are trying to ignore in
        elif(guild != ctx.guild.id and ctx.message.author.id != TNMN):
            await ctx.send("You do not have permission to ignore this person in that guild")
        #Move onto ignoring the person
        else:
            nukeArrayLocal = [nukeArray[0], nukeArray[1]] #Duplicate list for saving to file purposes
            #Check if they are already ignored
            if(user.id in nukeArray[0] and
                    nukeArray[1][nukeArray[0].index(user.id)] == guild):
                await ctx.send(f"User {user.mention} is already nuke ignored in server {nukeArrayLocal[1][nukeArrayLocal[0].index(user.id)]}")
            #Add person to ignore list
            else:
                nukeArrayLocal[0].append(user.id)
                nukeArrayLocal[1].append(guild)
                #Fix the nukeIgnore.py file
                with open("nukeIgnore.py", 'r+') as file:
                    file.truncate(0)
                    string = "nukeArray = [" +str(nukeArrayLocal[0])+"," +str(nukeArrayLocal[1])+"]"
                    file.write(string)
                    file.close()
                if(guild == "ALL"):
                    await ctx.send(f"Added user {user.mention} to nuke ignore in ALL guilds")
                else:
                    await ctx.send(f"Added user {user.mention} to nuke ignore in guild **{ctx.guild}**")

    @commands.command()
    @commands.check(is_admin)
    async def delNukeIgnore(self, ctx: commands.Context, user: discord.Member = None, guild: str = None):
        """ Remove person from ignore list """
        #Make sure user isn't none so the bot doesn't die
        if user is None:
            user = ctx.message.author
        #Make sure guild isn't none so bot doesn't die

        if guild is None:
            guild = ctx.guild.id

        if(guild != ctx.guild.id and ctx.message.author.id != TNMN):
            await ctx.send("You do not have permission to unignore this person in that guild")
        else:
            nukeArrayLocal2 = [nukeArray[0], nukeArray[1]]
            if(user.id in nukeArray[0] and
                    nukeArray[1][nukeArray[0].index(user.id)] == guild):
                nukeArrayLocal2[1].pop(nukeArrayLocal2[0].index(user.id))

                nukeArrayLocal2[0].remove(user.id)
                with open("nukeIgnore.py", 'r+') as file:
                    file.truncate(0)
                    string = "nukeArray = [" +str(nukeArrayLocal2[0])+"," +str(nukeArrayLocal2[1])+"]"
                    file.write(string)
                    file.close()

                await ctx.send(f"Added user {user.mention} to nuke ignore in guild **{ctx.guild}**")
            else:
                await ctx.send(f"User {user.mention} is already nuke unignored in that server")

    @commands.command(aliases=['addLDLStaff'],hidden=True)
    @commands.check(is_admin)
    #####################################
    #Add a person as staff on LDL server#
    #####################################
    async def addLdlStaff(self, ctx: commands.Context, user: discord.Member = None):
        """ Add person as staff on LDL server """
        # Written by Nerd#2021

        # Check if user is none so bot doesn't crash
        if user is None:
            user = ctx.message.author

        # Make sure person isn't trying to add themself or TNMN as staff
        if (user.id == ctx.message.author.id or user.id == TNMN):
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You cannot add this person as staff!", inline=True)
            await ctx.send(embed = embed)

        elif (ctx.message.guild.id != LDL_server):
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You cannot add people as staff in a different server!", inline=True)
            await ctx.send(embed=embed)

        # Move onto adding the person
        else:
            # Check if they are already staff
            if (user.id in ldl_staff[0]):
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"User {user.mention} is already staff in the LDL server!", inline=True)
                await ctx.send(embed=embed)
            # Add person to ignore list
            else:
                ldl_staffLocal = [ldl_staff[0], ldl_staff[1]]  # Duplicate list for saving to file purposes

                ldl_staffLocal[0].append(user.id)
                ldl_staffLocal[1].append(user.display_name)
                # Fix the ldl_staff.py file
                with open("ldl_staff.py", 'r+') as file:
                    file.truncate(0)
                    string = "ldl_staff = [" + str(ldl_staffLocal[0]) + "," + str(ldl_staffLocal[1]) + "]"
                    file.write(string)
                    file.close()
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**Success**", value=f"User {user.mention} has been added as LDL server staff!",inline=True)
                await ctx.send(embed=embed)

    @commands.command(aliases=['delLDLStaff'],hidden=True)
    @commands.check(is_admin)
    async def delLdlStaff(self, ctx: commands.Context, user: discord.Member = None):
        """ Remove person from ignore list """
        # Make sure user isn't none so the bot doesn't die
        if user is None:
            user = ctx.message.author

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
                embed.add_field(name="**Success**", value=f"Deleted {user.mention} from staff list in LDL server", inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"User {user.mention} is not staff in the LDL server", inline=True)
                await ctx.send(embed=embed)

    @commands.command(aliases=['getLDLStaff'],hidden=True)
    @commands.check(is_admin)
    async def getLdlStaff(self, ctx: commands.Context):
        embed = discord.Embed(color=ctx.author.color.value)
        embed.add_field(name="Staff List", value=ldl_staff[1], inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['createAdmin'],hidden=True)
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
            await ctx.send(voters)


def setup(bot):
    bot.add_cog(Discord_Info(bot))
    bot.add_cog(Locked(bot))
    bot.add_cog(Useful(bot))




