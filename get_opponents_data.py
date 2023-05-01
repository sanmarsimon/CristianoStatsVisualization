"""This file contains a function to get top 15 opponents based on the number of matches played"""

import pandas as pd
MATCHES_PATHFILE = "./datasets/matches/"


def get_opponents():
    """Reads in data from CSV files containing match data for football teams, aggregates the total number of goals scored
    and conceded, and the number of matches played against each opponent, and returns a sorted dataframe with the top 15 opponents.
    
    Returns:
        pandas.DataFrame: A dataframe with columns 'Adversaire', 'Buts', 'PD', and 'Matches', where 'Adversaire' indicates the name of the opponent team, 'Buts' indicates the total number of goals scored against the opponent, 'PD' indicates the total number of goals conceded, and 'Matches' indicates the number of matches played against the opponent.
    """
    # Initialize an empty dataframe to hold the data
    df = pd.DataFrame()

    # Iterate over the years 2002 to 2022
    for i in range(2002, 2023):
        # Read in the CSV file for the current year
        current_df = pd.read_csv(MATCHES_PATHFILE + str(i) + "-" + str(i+1) + ".csv")[['Date', 'Adversaire', 'Buts', 'PD']]
        # Concatenate the current year's dataframe with the existing dataframe
        df = pd.concat([df, current_df])

    # Drop any rows where the 'Date' column is empty
    df = df.dropna(subset=['Date'])

    # Replace any empty values in the 'PD' column with 0
    df['PD'].fillna(0, inplace=True)

    # Group the dataframe by team and aggregate the total goals scored and conceded, as well as the number of matches played
    team_stats = df.groupby('Adversaire').agg({'Buts': 'sum', 'PD': 'sum', 'Date': 'count'})

    # Rename the 'Date' column to 'Matches'
    team_stats.rename(columns={'Date': 'Matches'}, inplace=True)

    # Sort the resulting dataframe by the number of matches played, and select the top 15 opponents
    team_stats = team_stats.sort_values('Matches', ascending=False)
    team_stats = team_stats.iloc[:10].reset_index()

    # Return the final dataframe
    return team_stats
