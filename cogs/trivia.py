import discord
from discord.ext import commands

from nukeIgnore import *
from bot import *
import logging
import discord
from discord.ext import commands
from bot import *
import random
import asyncio
from permissions import *
from triviaCategoriesList import triviaCategoriesList
from airportCodesTrivia import airportCodesList

maxTriviaQuestions = len(airportCodesList[0])
numUnansweredMax = 3


async def getNumQuestions(self, ctx, maxQuestions, check):
    """Get the number of questions for a trivia game"""

    embed = discord.Embed(title="Trivia",
                          description=f"How many questions would you like? You can have up to {maxTriviaQuestions} questions",
                          color=ctx.message.author.top_role.color)  # Create question embed
    await ctx.send(embed=embed)  # Send embed
    try:

        msg = await client.wait_for('message', timeout=15.0, check=check) #Get response from user

        if int(msg.content) < 1 or int(msg.content) > maxTriviaQuestions:
            embed = discord.Embed(title="ERROR",
                                  description=f"Having a trivia game with {msg.content} number of questions is not valid at the moment. Please try again and enter a number between 1 and 10.",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:
            return int(msg.content)
    except asyncio.TimeoutError: #Timeout
        embed = discord.Embed(title="ERROR",
                              description=f"Trivia Start timed out. Please try again and send a message quicker next time!",
                              color=ctx.message.author.top_role.color)  # Create error embed
        await ctx.send(embed=embed)  # Send embed
        return

async def getCategory(self, ctx, category, check):

    embed = discord.Embed(title="Trivia", description=f"Please select a trivia category from the following categories:",
                          color=ctx.message.author.top_role.color)  # Create embed
    i = 1
    for category in triviaCategoriesList:
        embed.add_field(name=i, value=category, inline=True)  # Set title for first embed
        i += i
    await ctx.send(embed=embed)  # Send embed

    try:
        msg = await client.wait_for('message', timeout=15.0, check=check)

        if int(msg.content) < 1 or int(msg.content) > i:
            embed = discord.Embed(title="ERROR",
                                  description=f"Category **{category[int(msg.content)]}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:
            return category[int(msg.content)]

    except asyncio.TimeoutError:
        embed = discord.Embed(title="ERROR",
                              description=f"Trivia Start timed out. Please try again and send a message quicker next time!",
                              color=ctx.message.author.top_role.color)  # Create embed
        await ctx.send(embed=embed)  # Send embed
        return


async def airportCodesTrivia(self, ctx, questions, check, originalChannel):
    listOfQuestions = []
    correctAnswers = [[],[]]
    numUnanswered = 0
    x = 0

    while x < questions:
        answeredThisQuestion = [] #Variable for those who have answered this question so they can't guess again

        num = random.randint(0, len(airportCodesList[0])-1)
        if num not in listOfQuestions:
            listOfQuestions.append(num)
            embed = discord.Embed(title=f"Question {x+1}", description=f"What is the airport code for **{airportCodesList[0][num]}**",
                                  color=ctx.message.author.top_role.color)  # Create embed
            listOfAnswers = []
            counter = 0
            while counter < 3:
                num2 = random.randint(0, len(airportCodesList[0])-1)
                if num2 in listOfAnswers or num2 == num:
                    pass
                else:
                    listOfAnswers.append(num2)
                    counter = counter +1

            placementOfRightAnswer = random.randint(1, 4)
            counterWrongAnswer = 0

            counter2 = 0

            while counter2 < 4:
                if counter2 == placementOfRightAnswer:
                    embed.add_field(name=counter2, value=airportCodesList[1][num], inline=True)  #Get right answer added
                    counter2+=1
                else:
                    embed.add_field(name=counter2, value=airportCodesList[1][listOfAnswers[counterWrongAnswer]], inline=True)  # Set title for first embed
                    counterWrongAnswer+=1
                    counter2+=1
            await ctx.send(embed=embed)

            def checkCustom(message: discord.Message):
                if message.channel == originalChannel and int(message.content) == placementOfRightAnswer:
                    return True
                else:
                    return False

            await ctx.send("E")
            try:
                msg = await client.wait_for('message', timeout=15.0, check=checkCustom)
                embed = discord.Embed(title="Trivia",
                                      description=f"{msg.author.mention} has won this round!",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed
                if msg.author.id not in correctAnswers:
                    correctAnswers[0].append(msg.author.id)
                    correctAnswers[1].append(1)
                else:
                    await ctx.send(f"Current correct answers is {correctAnswers[1][correctAnswers[0].index[msg.author.id]]}")
                    correctAnswers[1][correctAnswers[0].index[msg.author.id]] += 1

            except asyncio.TimeoutError:  # Timeout
                embed = discord.Embed(title="Trivia",
                                      description=f"Question timed out! No one answered correctly!",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed

        x+=1

    counter = 0
    highestScore = 0
    highestScoreUser = 0

    while counter < len(correctAnswers[0]):
        if correctAnswers[1][counter] > highestScore:
            highestScore = correctAnswers[1][counter]
            highestScoreUser = correctAnswers[0][counter]
            await ctx.send(highestScoreUser)

        counter += 1

    embed = discord.Embed(title="Trivia",
                          description=f"Game over! The winner was <@{highestScoreUser}> with {highestScore} answers correct! That's a {highestScore/questions*100}% correct rate!",
                          color=ctx.message.author.top_role.color)  # Create embed
    await ctx.send(embed=embed)  # Send embed

class Trivia(commands.Cog):
    """
    Trivia related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['triviacategories'])
    async def triviaCategories(self, ctx):

        embed = discord.Embed(title="Trivia", description=f"The available trivia categories are:",
                              color=ctx.message.author.top_role.color) #Create embed
        i = 1
        for category in triviaCategoriesList:
            embed.add_field(name=i, value=category, inline=True) #Set title for first embed
            i+=i
        await ctx.send(embed=embed) #Send embed

    @commands.command(aliases=['triviastart'])
    async def triviaStart(self, ctx, category: str = None):
        msg = 0

        def check(message: discord.Message):
            return message.channel == ctx.channel



        if category is None:

            categorySelected = getCategory(self=self, ctx=ctx, category=category, check=check)
            numQuestions = await getNumQuestions(self=self, ctx=ctx, maxQuestions=maxTriviaQuestions, check=check)
            await ctx.send(numQuestions)
            await airportCodesTrivia(self=self, ctx=ctx, questions=numQuestions, check=check, originalChannel= ctx.message.channel)


        elif category not in triviaCategoriesList:
            embed = discord.Embed(title="ERROR",
                                  description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed

        else:
            numQuestions = await getNumQuestions(self=self, ctx=ctx, maxQuestions=maxTriviaQuestions, check=check)
            await ctx.send(numQuestions)
            await airportCodesTrivia(self=self, ctx=ctx, questions=numQuestions, check=check, originalChannel= ctx.message.channel)

def setup(bot):
    bot.add_cog(Trivia(bot))