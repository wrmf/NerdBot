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

#from NerdBot.airportCodesTrivia import airportCodesList

maxTriviaQuestions = len(airportCodesList[0])


async def getNumQuestions(self, ctx, maxQuestions):
    """Get the number of questions for a trivia game"""
    embed = discord.Embed(title="Trivia",
                          description=f"How many questions would you like? You can have up to {maxTriviaQuestions} questions",
                          color=ctx.message.author.top_role.color)  # Create question embed
    await ctx.send(embed=embed)  # Send embed
    try:

        msg = await client.wait_for('message', timeout=15.0) #Get response from user

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

async def getCategory(self, ctx, category):
    embed = discord.Embed(title="Trivia", description=f"Please select a trivia category from the following categories:",
                          color=ctx.message.author.top_role.color)  # Create embed
    i = 1
    for category in triviaCategoriesList:
        embed.add_field(name=i, value=category, inline=True)  # Set title for first embed
        i += i
    await ctx.send(embed=embed)  # Send embed

    try:
        msg = await client.wait_for('message', timeout=15.0)

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


async def airportCodesTrivia(self, ctx, questions):
    await ctx.send("I got to the function")
    listOfQuestions = []
    for x in range(0, questions):
        num = random.randint(1, len(airportCodesList[0]))
        if num not in listOfQuestions:
            listOfQuestions.append(num)
            embed = discord.Embed(title=f"Question {x}", description=f"What is the airport code for **{airportCodesList[0][num]}**",
                                  color=ctx.message.author.top_role.color)  # Create embed
            listOfAnswers = []
            await ctx.send("generatedListOfAnswers")
            for counter in range(0, 4):
                num2 = random.randint(0, maxTriviaQuestions+1)
                await ctx.send(num2)
                if num2 in listOfAnswers or num2 == num:
                    counter-=1
                else:
                    listOfAnswers.append(num2)

            placementOfRightAnswer = random.randint(1, 4)
            await ctx.send(f"Placement of right answer is {placementOfRightAnswer}")
            await ctx.send(f"Wrong answer list is {listOfAnswers}")
            counterWrongAnswer = 0

            for counter2 in range (1, 5):
                if counter2 == placementOfRightAnswer:
                    embed.add_field(name=counter2, value=airportCodesList[1][num], inline=True)  #Get right answer added
                else:
                    embed.add_field(name=counter2, value=airportCodesList[1][listOfAnswers[counterWrongAnswer]], inline=True)  # Set title for first embed
                    counterWrongAnswer+=1
            await ctx.send(embed=embed)

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

        if category is None:

            categorySelected = getCategory(self=self, ctx=ctx, category=category)
            numQuestions = await getNumQuestions(self=self, ctx=ctx, maxQuestions=maxTriviaQuestions)
            await ctx.send(f"number of questions is {numQuestions}")
            await airportCodesTrivia(self=self, ctx=ctx, questions=numQuestions)


        elif category not in triviaCategoriesList:
            embed = discord.Embed(title="ERROR",
                                  description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed

        else:
            numQuestions = await getNumQuestions(self=self, ctx=ctx, maxQuestions=maxTriviaQuestions)
            await ctx.send(f"number of questions is {numQuestions}")
            await airportCodesTrivia(self=self, ctx=ctx, questions=numQuestions)

def setup(bot):
    bot.add_cog(Trivia(bot))