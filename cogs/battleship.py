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

class Trivia(commands.Cog):
    """
    Trivia related commands
    """

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Battleship(bot))

# rows = ['1️⃣', '2️⃣', '3️⃣', 4️⃣, 5️⃣, '6️⃣', '7️⃣', 8️⃣, 9️⃣, '🔟']
# columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'] #TODO put in proper column labels with lettered emojis
#
# class location():
#     x = 0
#     y = 0
#
#     def location(varX, varY):
#         x = varX
#         y = varY
#
#     def getX(self):
#         return x
#
#     def getY(self):
#         return y
#
# class board():
#     size = 10
#
#
#     class gamePiece():
#         class ship():
#             pass
#
#
#
#
# async def getNextMove(self, ctx, originalChannel: int, originalUser: int):
#     pass
#
# async def takeNextMove(self, ctx, originalChannel: int, originalUser: int):
#     pass
#
# async def createBoard(self, ctx, originalChannel: int, originalUser: int):
#     embed = discord.Embed(title="ERROR",
#                           description=f"Unknown category somehow. Contact Nerd#2022",
#                           color=ctx.message.author.top_role.color)  # Create question embed
#     await ctx.send(embed=embed)  # Send embed