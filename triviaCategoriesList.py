from trivia.triviaElements import triviaElementsList
from airportCodes import airportCodesList
import pandas as pd

# # Read in CSV for airport code trivia
# columns = ["City", "Code"]  # Columns for pandas array
# fileNames = ["airportCodes.csv"]
# airportCodesTriviaDataframe = pd.read_csv(fileNames, header=None, delimiter="(", names=columns)
# airportCodesTriviaDataframe["Code"] = airportCodesTriviaDataframe["Code"].str[:-1]  # Delete ) from end of string
# airportCodesTriviaDataframe.sort_values("Code")  # Sort values by code... does this do anything?

triviaCategoriesList = [["airport codes", "airport names", "elements"], [airportCodesList[0], airportCodesList[1], triviaElementsList[0]]]