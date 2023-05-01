""" This file contains a function to get to assisting players """

import pandas as pd
from utils import get_data_from_file
GOALS_PATHFILE = "./datasets/cristiano/goals.xlsx"

def get_top_assisting_players():
    """
    Loads data about goals and assists, selects relevant columns,
    drops missing values in the assists column, counts the number of
    assists per player, keeps only the top ten players with the most
    assists, and sorts them by player name.
    
    Returns:
        pandas.DataFrame: A DataFrame containing information about the top
        ten players with the highest number of assists.
    """
   # Load data and select only relevant columns
    goals_data = get_data_from_file(GOALS_PATHFILE)
    goals_data = goals_data[['Clt', 'Passe décisive']]

    # Drop rows with missing values in the 'Passe décisive' column
    goals_data.dropna(subset=['Passe décisive'], inplace=True)

    # Count number of assists per player and sort in descending order
    assists_data = goals_data.groupby('Passe décisive').agg(assists_count=('Clt', 'count')).sort_values('assists_count', ascending=False).reset_index()

    # Keep only the top ten players with the highest number of assists and sort by player name
    top_assisting_players = assists_data.nlargest(10, 'assists_count').sort_values('Passe décisive')
    
    return top_assisting_players