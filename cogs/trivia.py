import discord
from discord.ext import commands

from nukeIgnore import *
import logging
import discord
from discord.ext import commands
import random
import asyncio
from permissions import *
from triviaCategoriesList import triviaCategoriesList
import importlib
from airportCodes import airportCodesList
from trivia.triviaElements import triviaElementsList
from trivia.LDLTriviaQuestions import LDLTriviaQuestions
from bot import *

numUnansweredMax = 3


async def getNumQuestions(self, ctx, check, category):
    """Get the number of questions for a trivia game"""

    if category in triviaCategoriesList[0]:
        maxTriviaQuestions = len(triviaCategoriesList[1][triviaCategoriesList[0].index(category)])
    else:
        maxTriviaQuestions = 0
        embed = discord.Embed(title="ERROR",
                              description=f"Unknown category somehow. Contact Nerd#2021",
                              color=ctx.message.author.top_role.color)  # Create question embed
        await ctx.send(embed=embed)  # Send embed

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
    for category in triviaCategoriesList[0]:
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


async def startTrivia(self, ctx, questions, originalChannel, question, questionList, answerList):
    listOfQuestions = []
    correctAnswers = [[],[]]
    x = 0

    while x < questions: #Multiple questions

        thisQuestionAnswers = []

        num = random.randint(0, len(questionList) - 1) #Correct answer

        while num in listOfQuestions: #Make sure this question has not been asked already this game
            num = random.randint(0, len(questionList) - 1)
        listOfQuestions.append(num) #Add correct answer
        embed = discord.Embed(title=f"Question {(x)+1}", description=f"{question} **{questionList[num]}**?",
                              color=ctx.message.author.top_role.color)  # Create embed

        listOfAnswers = [] #Wrong answer array
        counter = 0 #Counter for wrong answer number

        while counter < 3:
            num2 = random.randint(0, (len(questionList)-1)) #Generate location
            if num2 in listOfAnswers or num2 == num:
                pass #Do nothing if that answer has already been selected
            else:
                listOfAnswers.append(num2) #Add to list
                counter+=1 #Increment to make sure we only get 3 wrong answers

        placementOfRightAnswer = random.randint(0, 3) #Randomly generate right answer location
        counterWrongAnswer = 0 #Counter for the number of wrong answers place (for wrong answer array)

        counter2 = 0

        while counter2 < 4: #Place answers in embed
            if counter2 == placementOfRightAnswer: #Place correct answer
                embed.add_field(name=counter2+1, value=answerList[num], inline=False)  #Get right answer added
                counter2+=1
            else: #Place wrong answers
                embed.add_field(name=counter2+1, value=answerList[listOfAnswers[counterWrongAnswer]], inline=False)  # Set title for first embed
                counterWrongAnswer+=1
                counter2+=1
        await ctx.send(embed=embed) #Send embed

        def checkCustom(message: discord.Message): #Check for message
            if message.channel == originalChannel and int(message.content) == placementOfRightAnswer+1 and message.author.id not in thisQuestionAnswers:
                return True
            else:
                thisQuestionAnswers.append(message.author.id)
                return False

        try:
            msg = await client.wait_for('message', timeout=15.0, check=checkCustom) #Wait on player answer
            embed = discord.Embed(title="Trivia",
                                  description=f"{msg.author.mention} has won this round!",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
            if msg.author.id not in correctAnswers[0]:
                correctAnswers[0].append(msg.author.id) #Add them to the correct answer list
                correctAnswers[1].append(1) #Add their score to the correct answer list
            else:
                correctAnswers[1][correctAnswers[0].index(msg.author.id)] += 1  #Increment number of correct answers by player

        except asyncio.TimeoutError:  # Timeout
            embed = discord.Embed(title="Trivia",
                                  description=f"Question timed out! No one answered correctly! The correct answer was {answerList[num]} (number {placementOfRightAnswer+1})!",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed

        x+=1

    highestScoreUser = [0] #Player(s) with highest score
    highestScore = 0 #highest score
    multipleUsers = False #Bool for if there was a tie or not

    for n in correctAnswers[0]: #Loop through everyone who got an answer correct
        if correctAnswers[1][correctAnswers[0].index(n)] > highestScore: #If they are the new high score
            multipleUsers = False #Set tie bool to false
            highestScoreUser.clear() #Clear array of people
            highestScore = correctAnswers[1][correctAnswers[0].index(n)] #Make sure highest score is correct
            highestScoreUser = n #Set highest score user
        elif correctAnswers[1][correctAnswers[0].index(n)] == highestScore: #If they tied
            multipleUsers = True #Tie bool to true
            highestScoreUser.append(n) #Add user to list

    if not multipleUsers: #Print solo win message if there was one winner
        if(highestScoreUser != 0):
            embed = discord.Embed(title="Trivia",
                                  description=f"Game over! The winner was <@{highestScoreUser}> with {highestScore} answers correct! That's a {highestScore / questions * 100}% correct rate!",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:
            embed = discord.Embed(title="Trivia",
                                  description=f"Game over! No one got any answers correct!",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
    else: #Print win message if there was a tie (supports up to a 25 way tie)
        embed = discord.Embed(title="Trivia",
                              description=f"Game over! The winners are:",
                              color=ctx.message.author.top_role.color)  # Create embed

        for n in highestScoreUser: #Loop through people to print out
            embed.add_field(title="Winner!", value=f"<@{n}>", inline=True) #Add people
        embed.add_field(title="~", value=f"They each had {highestScore} questions correct! That's a {highestScore/questions*100}% correct rate!", inline=True) #Embed stating score
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
        """
        Get a list of all available trivia categories
        @author Nerd#2021
        """

        embed = discord.Embed(title="Trivia", description=f"The available trivia categories are:",
                              color=ctx.message.author.top_role.color) #Create embed
        i = 1
        for category in triviaCategoriesList[0]:
            embed.add_field(name=i, value=category, inline=True) #Set title for first embed
            i+=i
        await ctx.send(embed=embed) #Send embed

    @commands.command(aliases=['triviastart', 'startTrivia', 'starttrivia'])
    async def triviaStart(self, ctx, category: str = None):
        """
        Start trivia game
        @param category: category to start the game in
        @author Nerd#2021
        """

        def check(message: discord.Message): #Check for getting the number of questions
            return message.channel == ctx.channel

        if category is None: #Error if the user did not provide a category
            embed = discord.Embed(title="ERROR",
                                  description=f"Please chose a category and try again",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
            return

        elif category.lower() not in triviaCategoriesList[0]: #error if category is not valid
            embed = discord.Embed(title="ERROR",
                                  description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
            return

        #else: #Run game
        category = category.lower()
        numQuestions = await getNumQuestions(self=self, ctx=ctx, check=check, category=category.lower()) #Get the number of questions
        if numQuestions is not None:
            if category == triviaCategoriesList[0][0]: #Airport Codes trivia
                await startTrivia(self=self, ctx=ctx, questions=numQuestions, originalChannel=ctx.message.channel,
                                  question="What is the airport code for", questionList=airportCodesList[0],
                                  answerList=airportCodesList[1])
                return
            elif category == triviaCategoriesList[0][1]: #Airport Codes trivia
                await startTrivia(self=self, ctx=ctx, questions=numQuestions, originalChannel=ctx.message.channel,
                                  question="What airport has code", questionList=airportCodesList[1],
                                  answerList=airportCodesList[0])
                return
            elif category == triviaCategoriesList[0][2]: #Elements trivia
                await startTrivia(self=self, ctx=ctx, questions=numQuestions, originalChannel=ctx.message.channel,
                                  question="What element has abbreviation", questionList=triviaElementsList[1],
                                  answerList=triviaElementsList[0])

    @commands.command(aliases=['addairport'])
    @commands.check(is_plane)
    async def addAirport(self, ctx: commands.Context, name: str, code: str):
        """
        Add airport name and code to trivia list
        @param name: name of airport to add
        @param code: code for the airport being added
        @author Nerd#2021
        """

        # Check if user is none so bot doesn't crash
        if name is None or code is None:
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You cannot set the name or code to be none", inline=True)
            await ctx.send(embed=embed)

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
                with open("airportCodes.py", 'r+') as file:
                    file.truncate(0)
                    string = "airportCodesList = [" + str(airportCodesListLocal[0]) + "," + str(airportCodesListLocal[1]) + "]"
                    file.write(string)
                    file.close()
                embed = discord.Embed(color=ctx.author.color.value)  # Make embed
                embed.add_field(name="**Success**", value=f"{name} Airport has been added!",
                                inline=True)  # Make sucess message
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed

    @commands.command(aliases=['addelement'])
    @commands.check(is_admin)
    async def addElement(self, ctx: commands.Context, name: str, abb: str):
        """
        Add airport name and code to trivia list
        @param name: name of airport to add
        @param abb: code for the airport being added
        @author Nerd#2021
        """

        # Check if user is none so bot doesn't crash
        if name is None or abb is None:
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You cannot set the name or abbreviation to be none", inline=True)
            await ctx.send(embed=embed)

        # Move onto adding the airport
        else:
            # Check if airport is already in the list
            if (name in triviaElementsList[0] or abb in triviaElementsList[1]):
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"{name} is already in the list",
                                inline=True)
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)
            # Add airport
            else:
                triviaElementsListLocal = [triviaElementsList[0],
                                         triviaElementsList[1]]  # Duplicate list for saving to file purposes

                triviaElementsListLocal[0].append(name)  # Add their ID
                triviaElementsListLocal[1].append(abb)  # Add their display name
                # Fix the ldl_staff.py file
                with open("trivia/triviaElements.py", 'r+') as file:
                    file.truncate(0)
                    string = "triviaElementsList = [" + str(triviaElementsListLocal[0]) + "," + str(
                        triviaElementsListLocal[1]) + "]"
                    file.write(string)
                    file.close()
                embed = discord.Embed(color=ctx.author.color.value)  # Make embed
                embed.add_field(name="**Success**", value=f"{name} has been added!",
                                inline=True)  # Make sucess message
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed

    @commands.command(aliases=['printquestions', 'triviaQuestions', 'triviaquestions'])
    @commands.check(is_owner)
    async def printQuestions(self, ctx: commands.Context, category: str = None):
        """
        Print out all of the questions for a specified category
        @param category: category to print questions from
        @author Nerd#2021
        """

        if category == None: #Make sure user entered a category
            embed = discord.Embed(title="ERROR",
                                  description=f"Please enter a category and try again",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        elif category not in triviaCategoriesList[0]: #Make sure category is valid
            embed = discord.Embed(title="ERROR",
                                  description=f"Category **{category}** is not a valid category. Please do ~triviaCategories for the full list of categories",
                                  color=ctx.message.author.top_role.color)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else: #Print it out
            embed = discord.Embed(title="Trivia",
                                  description=f"The questions in category {category} are:",
                                  color=ctx.message.author.top_role.color)  # Create embed
            counter = 1;
            list = triviaCategoriesList[1][triviaCategoriesList[0].index(category)]
            random.shuffle(list)
            for n in list: #Loop through questions
                embed.add_field(name=counter, value=f"{n}\n", inline=False)
                counter+=1 #Make sure
                if counter%25 == 0 and counter != 0:
                    embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                    await ctx.send(embed=embed)  # Send embed
                    embed = discord.Embed(title="Trivia",
                                          description=f"Embed ran out of space, continuing!",
                                          color=ctx.message.author.top_role.color)  # Create embed
                elif (list.index(n) == len(list) - 1):
                    embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                    await ctx.send(embed=embed)  # Send embed

    @commands.command(aliases=['addldlquestion', 'addLDLquestion'])
    @commands.check(is_plane)
    async def addLDLQuestion(self, ctx: commands.Context, question: str, answer: str, wrong1: str, wrong2: str, wrong3: str, timeout: int):
        """
        Add command to LDL trivia night
        @param question: the full question
        @param answer: the answer
        @param timeout: the timeout
        @author Nerd#2021
        """

        # Check if user is none so bot doesn't crash
        if question is None or answer is None or timeout is None:
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value="You gave an empty answer", inline=True)
            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed)

        # Move onto adding the airport
        else:

            thisQuestion = [answer, wrong1, wrong2, wrong3]

            # Check if airport is already in the list
            if (question in LDLTriviaQuestions[0]):
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"{question} is already in the list",
                                inline=True)
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)
            # Add airport
            else:
                LDLTriviaQuestionsLocal = [LDLTriviaQuestions[0],
                                           LDLTriviaQuestions[1], LDLTriviaQuestions[2]]  # Duplicate list for saving to file purposes


                LDLTriviaQuestionsLocal[0].append(question)  # Add question
                LDLTriviaQuestionsLocal[1].append(thisQuestion)  # Add answer
                LDLTriviaQuestionsLocal[2].append(timeout)  # Added timeout

                # Fix the ldl_staff.py file
                with open("trivia/LDLTriviaQuestions.py", 'r+') as file:
                    file.truncate(0)
                    string = "LDLTriviaQuestions = [" + str(LDLTriviaQuestionsLocal[0]) + "," + str(
                        LDLTriviaQuestionsLocal[1]) + "," + str(LDLTriviaQuestionsLocal[2])+ "]"
                    file.write(string)
                    file.close()
                embed = discord.Embed(color=ctx.author.color.value)  # Make embed
                embed.add_field(name="**Success**", value=f"**'{question}'** has been added!",
                                inline=True)  # Make sucess message
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed

    @commands.command(aliases=['delldlquestion', 'delLDLquestion'])
    @commands.check(is_plane)
    async def delLDLQuestion(self, ctx: commands.Context, answer: str):
        """
        Del command to LDL trivia night
        @param answer: the answer
        @author Nerd#2021
        """

        # Check if user is none so bot doesn't crash
        if answer is None:
            embed = discord.Embed(color=ctx.author.color.value)
            embed.add_field(name="**ERROR**", value=f"{answer} is not a valid question",
                            inline=True)
            embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
            await ctx.send(embed=embed)

        # Move onto adding the airport
        else:
            # Check if airport is already in the list
            if (answer not in LDLTriviaQuestions[1]):
                embed = discord.Embed(color=ctx.author.color.value)
                embed.add_field(name="**ERROR**", value=f"{answer} is not in the answer list",
                                inline=True)
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)
            # Add airport
            else:
                LDLTriviaQuestionsLocal = [LDLTriviaQuestions[0],
                                           LDLTriviaQuestions[1],
                                           LDLTriviaQuestions[2]]  # Duplicate list for saving to file purposes

                LDLTriviaQuestionsLocal[0].pop(LDLTriviaQuestionsLocal[1].index(answer)) # Remove question
                LDLTriviaQuestionsLocal[1].remove(answer)  # Add answer
                LDLTriviaQuestionsLocal[2].pop(LDLTriviaQuestionsLocal[1].index(answer))  # Remove timeout
                # Fix the ldl_staff.py file
                with open("trivia/LDLTriviaQuestions.py", 'r+') as file:
                    file.truncate(0)
                    string = "LDLTriviaQuestions = [" + str(LDLTriviaQuestionsLocal[0]) + "," + str(
                        LDLTriviaQuestionsLocal[1]) + "," + str(LDLTriviaQuestionsLocal) + "]"
                    file.write(string)
                    file.close()
                embed = discord.Embed(color=ctx.author.color.value)  # Make embed
                embed.add_field(name="**Success**", value=f"**'{answer}'** has been removed!",
                                inline=True)  # Make sucess message
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed

    @commands.command(aliases=['ldlQuestions', 'ldlquestions', 'printldlquestions'])
    @commands.check(is_plane)
    async def printLDLQuestions(self, ctx: commands.Context):
        """
        Print out all of the questions for a specified category
        @param category: category to print questions from
        @author Nerd#2021
        """

        embed = discord.Embed(title="Trivia",
                              description=f"The questions for the LDL trivia night are:",
                              color=ctx.message.author.top_role.color)  # Create embed
        counter = 1;
        list = LDLTriviaQuestions[0]
        random.shuffle(list)
        for n in list: #Loop through questions
            embed.add_field(name=counter, value=f"{n}\n", inline=False)
            counter+=1 #Make sure
            if counter%25 == 0 and counter != 0:
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed
                embed = discord.Embed(title="Trivia",
                                      description=f"Embed ran out of space, continuing!",
                                      color=ctx.message.author.top_role.color)  # Create embed
            elif (list.index(n) == len(list) - 1):
                embed.set_footer(text=f"Message requested by {ctx.author}")  # Footer
                await ctx.send(embed=embed)  # Send embed

    @commands.command(aliases=['startLDLtrivia', 'startldltrivia'])
    async def startLDLTrivia(self, ctx):
        """
        Start trivia game (for ldl Trivia Night)
        @author Nerd#2021
        """

        def check(message: discord.Message):  # Check for getting the number of questions
            return message.channel == ctx.channel

        numQuestions = len(LDLTriviaQuestions[0])-1

        listOfQuestions = []
        correctAnswers = [[], []]
        counterx = 0

        while counterx < numQuestions:  # Multiple questions

            thisQuestionAnswers = []

            num = random.randint(0, len(LDLTriviaQuestions) - 1)  # Correct answer

            while num in listOfQuestions:  # Make sure this question has not been asked already this game
                num = random.randint(0, len(LDLTriviaQuestions) - 1)
            listOfQuestions.append(num)  # Add correct answer
            embed = discord.Embed(title=f"Question {(counterx) + 1}", description=f"{LDLTriviaQuestions[0][num]}?",
                                  color=ctx.message.author.top_role.color)  # Create embed

            listOfAnswers = []  # Wrong answer array
            counter = 0  # Counter for wrong answer number

            while counter < 3:
                num2 = random.randint(0, (len(LDLTriviaQuestions[0]) - 1))  # Generate location
                if num2 in listOfAnswers or num2 == num:
                    pass  # Do nothing if that answer has already been selected
                else:
                    listOfAnswers.append(num2)  # Add to list
                    counter += 1  # Increment to make sure we only get 3 wrong answers

            placementOfRightAnswer = random.randint(0, 3)  # Randomly generate right answer location
            counterWrongAnswer = 0  # Counter for the number of wrong answers place (for wrong answer array)

            counter2 = 0

            while counter2 < 4:  # Place answers in embed
                if counter2 == placementOfRightAnswer:  # Place correct answer
                    embed.add_field(name=counter2 + 1, value=LDLTriviaQuestions[1][num][0], inline=False)  # Get right answer added
                    counter2 += 1
                else:  # Place wrong answers
                    embed.add_field(name=counter2 + 1, value=LDLTriviaQuestions[1][num][counterWrongAnswer+1],
                                    inline=False)  # Set title for first embed
                    counterWrongAnswer += 1
                    counter2 += 1
            await ctx.send(embed=embed)  # Send embed

            def checkCustom(message: discord.Message):  # Check for message
                if message.channel == ctx.message.channel and int(
                        message.content) == placementOfRightAnswer + 1 and message.author.id not in thisQuestionAnswers:
                    return True
                else:
                    thisQuestionAnswers.append(message.author.id)
                    return False

            try:
                msg = await client.wait_for('message', timeout=LDLTriviaQuestions[2][num], check=checkCustom)  # Wait on player answer
                embed = discord.Embed(title="Trivia",
                                      description=f"{msg.author.mention} has won this round!",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed
                if msg.author.id not in correctAnswers[0]:
                    correctAnswers[0].append(msg.author.id)  # Add them to the correct answer list
                    correctAnswers[1].append(1)  # Add their score to the correct answer list
                else:
                    correctAnswers[1][
                        correctAnswers[0].index(msg.author.id)] += 1  # Increment number of correct answers by player

            except asyncio.TimeoutError:  # Timeout
                embed = discord.Embed(title="Trivia",
                                      description=f"Question timed out! No one answered correctly! The correct answer was {LDLTriviaQuestions[1][num]} (number {placementOfRightAnswer + 1})!",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed

            counterx += 1

        highestScoreUser = [0]  # Player(s) with highest score
        highestScore = 0  # highest score
        multipleUsers = False  # Bool for if there was a tie or not

        for n in correctAnswers[0]:  # Loop through everyone who got an answer correct
            if correctAnswers[1][correctAnswers[0].index(n)] > highestScore:  # If they are the new high score
                multipleUsers = False  # Set tie bool to false
                highestScoreUser.clear()  # Clear array of people
                highestScore = correctAnswers[1][correctAnswers[0].index(n)]  # Make sure highest score is correct
                highestScoreUser = n  # Set highest score user
            elif correctAnswers[1][correctAnswers[0].index(n)] == highestScore:  # If they tied
                multipleUsers = True  # Tie bool to true
                highestScoreUser.append(n)  # Add user to list

        if not multipleUsers:  # Print solo win message if there was one winner
            if (highestScoreUser != 0):
                embed = discord.Embed(title="Trivia",
                                      description=f"Game over! The winner was <@{highestScoreUser}> with {highestScore} answers correct! That's a {highestScore / numQuestions * 100}% correct rate!",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed
            else:
                embed = discord.Embed(title="Trivia",
                                      description=f"Game over! No one got any answers correct!",
                                      color=ctx.message.author.top_role.color)  # Create embed
                await ctx.send(embed=embed)  # Send embed
        else:  # Print win message if there was a tie (supports up to a 25 way tie)
            embed = discord.Embed(title="Trivia",
                                  description=f"Game over! The winners are:",
                                  color=ctx.message.author.top_role.color)  # Create embed

            for n in highestScoreUser:  # Loop through people to print out
                embed.add_field(title="Winner!", value=f"<@{n}>", inline=True)  # Add people
            embed.add_field(title="~",
                            value=f"They each had {highestScore} questions correct! That's a {highestScore / numQuestions * 100}% correct rate!",
                            inline=True)  # Embed stating score
            await ctx.send(embed=embed)  # Send embed

        return

def setup(bot):
    bot.add_cog(Trivia(bot))