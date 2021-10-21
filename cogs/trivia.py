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
from airportCodesTriviaFile import airportCodesList
import importlib

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
                                  description=f"Having a trivia game with {msg.content} number of questions is not valid at the moment. Please try again and enter a number between 1 and {maxTriviaQuestions}.",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:
            return int(msg.content)
    except asyncio.TimeoutError: #Timeout
        embed = discord.Embed(title="ERROR",
                              description=f"Trivia Start timed out. Please try again and send a message quicker next time!",
                              color=ctx.message.author.top_role.color)  # Create error embed
        await ctx.send(embed=embed)  # Send embed
        return None

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


async def airportCodesTrivia(self, ctx, questions, originalChannel):
    listOfQuestions = []
    correctAnswers = [[],[]]
    x = 0

    while x < questions:
        num = random.randint(0, len(airportCodesList[0]) - 1)
        while num in listOfQuestions:
            num = random.randint(0, len(airportCodesList[0]) - 1)
        listOfQuestions.append(num)
        embed = discord.Embed(title=f"Question {(x)+1}", description=f"What is the airport code for **{airportCodesList[0][num]}**",
                              color=ctx.message.author.top_role.color)  # Create embed
        listOfAnswers = []
        counter = 0
        while counter < 3:
            num2 = random.randint(0, (len(airportCodesList[0])-1))
            if num2 in listOfAnswers or num2 == num:
                pass
            else:
                listOfAnswers.append(num2)
                counter+=1

        placementOfRightAnswer = random.randint(0, 3)
        counterWrongAnswer = 0

        counter2 = 0

        while counter2 < 4:
            if counter2 == placementOfRightAnswer:
                embed.add_field(name=counter2, value=airportCodesList[1][num], inline=False)  #Get right answer added
                counter2+=1
            else:
                embed.add_field(name=counter2, value=airportCodesList[1][listOfAnswers[counterWrongAnswer]], inline=False)  # Set title for first embed
                counterWrongAnswer+=1
                counter2+=1
        await ctx.send(embed=embed)

        def checkCustom(message: discord.Message):
            if message.channel == originalChannel and int(message.content) == placementOfRightAnswer:
                return True
            else:
                return False

        try:
            msg = await client.wait_for('message', timeout=15.0, check=checkCustom)
            embed = discord.Embed(title="Trivia",
                                  description=f"{msg.author.mention} has won this round!",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
            if msg.author.id not in correctAnswers[0]:
                correctAnswers[0].append(msg.author.id)
                correctAnswers[1].append(1)
            else:
                correctAnswers[1][correctAnswers[0].index(msg.author.id)] += 1

        except asyncio.TimeoutError:  # Timeout
            embed = discord.Embed(title="Trivia",
                                  description=f"Question timed out! No one answered correctly! The correct answer was {airportCodesList[1][num]} (number {placementOfRightAnswer})!",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed

        x+=1

    highestScoreUser = [0]
    highestScore = [0]
    multipleUsers = False

    for n in correctAnswers[0]:
        if correctAnswers[1][correctAnswers[0].index(n)] > highestScore[0]:
            multipleUsers = False
            highestScore.clear()
            highestScoreUser.clear()
            highestScore = correctAnswers[1][correctAnswers[0].index(n)]
            highestScoreUser = n
        elif correctAnswers[1][correctAnswers[0].index(n)] == highestScore[0]:
            multipleUsers = True
            highestScoreUser.append(n)
            highestScore.append(correctAnswers[1][correctAnswers[0].index(n)])

    if not multipleUsers:
        embed = discord.Embed(title="Trivia",
                              description=f"Game over! The winner was <@{highestScoreUser}> with {highestScore} answers correct! That's a {highestScore / questions * 100}% correct rate!",
                              color=ctx.message.author.top_role.color)  # Create embed
        await ctx.send(embed=embed)  # Send embed
    else:
        embed = discord.Embed(title="Trivia",
                              description=f"Game over! The winners are:",
                              color=ctx.message.author.top_role.color)  # Create embed

        for n in highestScoreUser:
            embed.add_field(title="Winner!", value=f"<@{n}>", inline=True)
        embed.add_field(title="~", value=f"each with {highestScore} questions correct! That's a {highestScore/questions*100}% correct rate!", inline=True)
        await ctx.send(embed=embed)  # Send embed

    return

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
            await airportCodesTrivia(self=self, ctx=ctx, questions=numQuestions, originalChannel= ctx.message.channel)


        elif category not in triviaCategoriesList:
            embed = discord.Embed(title="ERROR",
                                  description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed

        else:
            numQuestions = await getNumQuestions(self=self, ctx=ctx, maxQuestions=maxTriviaQuestions, check=check)
            if numQuestions is not None:
                await ctx.send(numQuestions)
                await airportCodesTrivia(self=self, ctx=ctx, questions=numQuestions, originalChannel= ctx.message.channel)

    @commands.command(aliases=['addairport'])
    @commands.check(is_mod)
    async def addAirport(self, ctx: commands.Context, name: str, code: str):
        """
        Add airport name and code to trivia list
        @author Nerd#2021
        """

        # Check if user is none so bot doesn't crash
        if name is None or code is None:
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You cannot set the name or code to be none", inline=True)
            await ctx.send(embed=embed)

        # Make sure person isn't trying to add themself or TNMN as staff
        #if (ctx.message.author.id != 308270212359258113 or ctx.message.author.id != 555207100603826177):
        #    embed = discord.Embed(color=ctx.author.color.value)
        #    embed.add_field(name="**ERROR**", value="You do not have permission to use this command", inline=True)
        #    await ctx.send(embed=embed)

        # Move onto adding the airport
        else:
            # Check if airport is already in the list
            if (name in airportCodesList[0] or code in airportCodesList[1]):
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"{name} Airport is already in the list",
                                inline=True)
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)
            # Add airport
            else:
                airportCodesListLocal = [airportCodesList[0], airportCodesList[1]]  # Duplicate list for saving to file purposes

                airportCodesListLocal[0].append(name)  # Add their ID
                airportCodesListLocal[1].append(code)  # Add their display name
                # Fix the ldl_staff.py file
                with open("airportCodesTriviaFile.py", 'r+') as file:
                    file.truncate(0)
                    string = "airportCodesList = [" + str(airportCodesListLocal[0]) + "," + str(airportCodesListLocal[1]) + "]"
                    file.write(string)
                    file.close()
                embed = discord.Embed(color=ctx.author.color.value)  # Make embed
                embed.add_field(name="**Success**", value=f"{name} Airport has been added!",
                                inline=True)  # Make sucess message
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed

def setup(bot):
    bot.add_cog(Trivia(bot))