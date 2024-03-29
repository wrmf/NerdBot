from trivia.triviaElements import triviaElementsList
from trivia.airportCodes import airportCodesList
import pandas as pd
import trivia

# Read in CSV for elements trivia
columns = ["Name", "Number"]  # Columns for pandas array
elementsDataframe = pd.read_csv("trivia/triviaElementsText.csv", header=None, delimiter="(", names=columns)
elementsDataframe["Number"] = elementsDataframe["Number"].str[:-1]  # Delete ) from end of string
elementsDataframe.sort_values("Number")  # Sort values by code... does this do anything?

# # Read in CSV for airport codes trivia
# columnsAirportCodes = ["Code", "Name", "Random"]
# airportCodesDataframe = pd.read_csv("trivia/airportCodesText.csv", header = None, delimiter='"', names=columnsAirportCodes)
# airportCodesDataframe.sort_values("Code") #Sort values by code... does this do anything?

triviaCategoriesList = [["airport codes", "airport names", "elements"], [airportCodesList[0], airportCodesList[1], elementsDataframe["Name"]]]