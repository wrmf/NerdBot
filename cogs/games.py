import discord
from discord.ext import commands
import random
from bot import *
from permissions import *
import asyncio
blankSquare = '|'
crossSquare = 'X'
circleSquare = 'O'

async def getCircle(ctx, user):
    embed = discord.Embed(title="TicTacToe",
                          description=f"User {user.mention} would you like to be circle or cross?",
                          color=ctx.message.author.top_role.color)  # Create error embed
    await ctx.send(embed=embed)  # Send embed
    def check(message: discord.Message):  # Check for getting the number of questions
        return message.channel == ctx.channel and message.author == user and (message.clean_content.lower() ==
                                                            'circle' or message.clean_content.lower() == 'cross')
    try:
        msg = await client.wait_for('message', timeout=30, check=check)  # Get response from user
        if 'circle' not in msg.clean_content.lower():
            embed = discord.Embed(title="TicTacToe",
                                  description=f"User {user.mention} has selected circle. {ctx.message.author.mention} "
                                              f"will be cross",
                                  color=ctx.message.author.top_role.color)  # Create error embed
            await ctx.send(embed=embed)  # Send embed
            return user
        elif 'cross' not in msg.clean_content.lower():
            embed = discord.Embed(title="TicTacToe",
                                  description=f"User {user.mention} has selected cross. {ctx.message.author.mention} "
                                              f"will be circle",
                                  color=ctx.message.author.top_role.color)  # Create error embed
            await ctx.send(embed=embed)  # Send embed
            return ctx.message.author
    except asyncio.TimeoutError:  # Timeout
        embed = discord.Embed(title="ERROR",
                              description=f"User {user.mention} did not select a symbol. Ending game",
                              color=ctx.message.author.top_role.color)  # Create error embed
        await ctx.send(embed=embed)  # Send embed
        return None

async def generateNewBoard():
    board = [[" ", "1", "2", "3"],["a", blankSquare, blankSquare, blankSquare],
             ["b", blankSquare, blankSquare, blankSquare], ["c", blankSquare, blankSquare, blankSquare]]
    return board

async def printBoard(board, embed):
    embed = discord.Embed(title=f"TicTacToe", description=f"{board[0]}\n, {board[1]}\n, {board[2]}\n, {board[3]}\n")
    return

async def checkRows(board):
    """
    Check rows of the TicTacToe board
    @return True if there is a win condition in rows, false if not
    @author Nerd#2022
    """
    if(board[1][1] != '|' and board[1][2] != '|' and board[1][3] != '|' and board[1][1] ==
            board[1][2] and board[1][1] == board[1][3]):
        return True
    elif (board[2][1] != '|' and board[2][2] != '|' and board[2][3] != '|' and board[2][1] ==
            board[2][2] and board[2][1] == board[2][3]):
        return True
    elif (board[3][1] != '|' and board[3][2] != '|' and board[3][3] != '|' and board[3][1] ==
            board[3][2] and board[3][1] == board[3][3]):
        return True
    else:
        return False

async def checkColumns(board):
    """
    Check columns of TicTacToe Board
    @return True if there is a win condition in rows, false if not
    @author Nerd#2022
    """
    if(board[1][1] != '|' and board[2][1] != '|' and board[3][1] != '|' and board[2][1] ==
            board[2][2] and board[2][1] == board[2][3]):
        return True
    elif (board[1][2] != '|' and board[2][2] != '|' and board[3][2] != '|' and board[1][2] ==
            board[2][2] and board[1][2] == board[3][2]):
        return True
    elif (board[1][3] != '|' and board[2][3] != '|' and board[3][3] != '|' and board[1][3] ==
            board[2][3] and board[1][3] == board[3][3]):
        return True
    else:
        return False

async def checkDiagonals(board):
    """
    Check diagonals of TicTacToe board
    @return True if there is a win condition in rows, false if not
    @author Nerd#2022
    """
    if(board[1][1] != '|' and board[2][2] != '|' and board[3][3] != '|' and board[1][1] == board[2][2] and
            board[1][1] == board[3][3]):
        return True
    elif (board[3][1] != '|' and board[2][2] != '|' and board[1][3] != '|' and board[3][1] == board[2][2] and
            board[3][1] == board[1][3]):
        return True
    else:
        return False


async def isGameOver(embed, board):
    return checkRows(board) and checkColumns(board) and checkDiagonals(board)

async def updateSquare(board, xCoord, yCoord, symbol):
    board[xCoord+1][yCoord+1] = symbol
    return board

async def makeMove(embed, board, crossUser, circleUser, lastX, lastY):
    """
    Make move (if game is not over)
    @return True if game is over, false if not
    @author Nerd#2022
    """
    if not isGameOver(embed, board):
        return True



class Games(commands.Cog):
    """
    Game commands
    @author Nerd#2022
    """

    blankSquare = '|'
    crossSquare = 'X'
    circleSquare = 'O'

    @commands.command()
    @commands.guild_only()
    async def challenge(self, ctx: commands.Context, user: discord.Member = None):
        """
        Challenges a user to TicTacToe. Format: ~challenge @user
        """

        await ctx.send(f"{user.mention}, {ctx.message.author.mention} has challenged you to TicTacToe. "
                       f"If you accept, please type 'yes' in the next 30 seconds")

        def check(message: discord.Message): #Check for getting the number of questions
            return message.channel == ctx.channel and message.author == user
        try:
            msg = await client.wait_for('message', timeout=30, check=check)  # Get response from user
            if 'yes' not in msg.clean_content.lower():
                embed = discord.Embed(title="ERROR",
                                      description=f"User {user.mention} did not say yes. Ending game",
                                      color=ctx.message.author.top_role.color)  # Create error embed
                await ctx.send(embed=embed)  # Send embed
                return None
        except asyncio.TimeoutError:  # Timeout
            embed = discord.Embed(title="ERROR",
                                  description=f"User {user.mention} did not respond. Ending game",
                                  color=ctx.message.author.top_role.color)  # Create error embed
            await ctx.send(embed=embed)  # Send embed
            return None

        embed = discord.Embed(title="Success!",
                              description=f"User {user.mention} accepted your challenge! Generating board!",
                              color=ctx.message.author.top_role.color)  # Create error embed
        gameMessage = await ctx.send(embed=embed)  # Send embed

        embed.set_footer(text='ID: {}'.format(gameMessage.id))

        #Get circle and cross
        circleUser = await getCircle(ctx, user)

        if circleUser == None: #Return none if no one chose circle/cross
            return None

        crossUser = None

        if circleUser == ctx.message.author:
            crossUser = user
        else:
            crossUser = ctx.message.author

        board = generateNewBoard()









def setup(bot):
    bot.add_cog(Games(bot))