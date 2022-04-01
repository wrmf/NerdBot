from trivia.triviaElements import triviaElementsList
from trivia.airportCodes import airportCodesList
import pandas as pd
import trivia.triviaElementsText
import trivia.airportCodesText

# Read in CSV for elements trivia
columns = ["Name", "Number"]  # Columns for pandas array
elementsDataframe = pd.read_csv("trivia/triviaElementsText.csv", header=None, delimiter="(", names=columns)
elementsDataframe["Number"] = elementsDataframe["Number"].str[:-1]  # Delete ) from end of string
elementsDataframe.sort_values("Number")  # Sort values by code... does this do anything?

# Read in CSV for airport codes trivia
airportCodesDataframe = pd.read_csv("", header = None, delimiter='"', names=columns)
airportCodesDataframe.sort_values("Code") #Sort values by code... does this do anything?

triviaCategoriesList = [["airport codes", "airport names", "elements"], [airportCodesList[0], airportCodesList[1], elementsDataframe["Name"]]]