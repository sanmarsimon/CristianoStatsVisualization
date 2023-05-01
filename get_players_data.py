"""This file contains several functions for processing and analyzing football players' statistics related to goals,
 shots, passes, shot percentage, and goal/assist stats."""
 
import pandas as pd
import utils
DATASETS_PATH = './datasets/'

def goal_ass_stats(player_name):
    """
    This function reads in a CSV file containing the player's stats,
    selects the columns for goals and assists per 90 minutes, and returns the resulting DataFrame.
    """
    # Read in the CSV file from the 'datasets' directory for the specified player
    df_goals_ass = pd.read_csv(DATASETS_PATH + player_name + '/stats.csv')
    
    # Format the DataFrame using the 'format_dataframe' function from the 'utils' module
    df_goals_ass = utils.format_dataframe(df_goals_ass)
    
    # Select the columns for goals and assists per 90 minutes
    goal_ass_stats = df_goals_ass.loc[:, ['Saison', 'Par90minutes.Buts', 'Par90minutes.PD']]
    
    # Convert the data types of the columns to 'float'
    goal_ass_stats.loc[:, 'Par90minutes.Buts'] = goal_ass_stats['Par90minutes.Buts'].astype(float)
    goal_ass_stats.loc[:, 'Par90minutes.PD'] = goal_ass_stats['Par90minutes.PD'].astype(float)
    
    # Return the resulting DataFrame
    return goal_ass_stats

def shot_stats(player_name):
    """This function takes a player's name as input and returns a pandas DataFrame containing
    shot creation statistics for that player
    
    Args:
        player_name (str): The name of the player whose shot creation stats are being queried.
        
    Returns:
        pandas DataFrame: A DataFrame containing the player's shot creation statistics.
    """
    
    # Load the shot creation dataset for the specified player, which is stored in a CSV file.
    # The CSV file is assumed to be stored in the DATASETS_PATH directory.
    df_shot = pd.read_csv(DATASETS_PATH + player_name + '/shot_creation.csv')[["Season", "SCA90"]]
    
    # Use .loc accessor to select only the relevant columns from the DataFrame
    df_shot = df_shot.loc[:, ["Season", "SCA90"]]
    
    # Return the DataFrame containing the shot creation statistics.
    return df_shot

def pass_stats(player_name):
    """
    This function reads csv file for a given player, formats the data,
    and returns a DataFrame with the player's season and total completion percentage.

    Args:
        player_name (str): The name of the player whose pass data is being analyzed.

    Returns:
        pandas.DataFrame: A DataFrame with the player's season and total completion percentage.
    """
    # Read in pass.csv file for the given player and format the data
    df_pass = pd.read_csv(DATASETS_PATH + player_name + '/pass.csv')
    df_pass = utils.format_dataframe(df_pass)

    # Use .loc accessor to select only the relevant columns from the DataFrame
    df_pass = df_pass.loc[:, ["Season", "Total.Cmp%"]]

    # Return the resulting DataFrame
    return df_pass
    
def group_last_5_years_data(df_shot, df_pass, df_shot_percentage, goal_ass_stats):
    """This function groups the last 5 years of data from several dataframes 
    and returns a new dataframe with the results.

    Args:
        df_shot (pandas DataFrame): a dataframe containing shot data
        df_pass (pandas DataFrame): a dataframe containing passing data
        df_shot_percentage (pandas DataFrame): a dataframe containing shot percentage data
        goal_ass_stats (pandas DataFrame): a dataframe containing goal and assist statistics

    Returns:
        pandas DataFrame: a new dataframe with the results
    """
    # select the last 5 rows of the shot dataframe
    df_shot = df_shot.tail(5)
    
    # select the last 5 rows of the passing dataframe
    df_pass = df_pass.tail(5)
    
    # select the last 5 rows of the shot percentage dataframe
    df_shot_percentage = df_shot_percentage.tail(5)
    
    # group the goal and assist statistics by season and sum them up
    group_by_season = goal_ass_stats.groupby(['Saison']).sum()
    
    # select the last 5 seasons and reset the index
    group_by_season = group_by_season.tail(5).reset_index()
    
    # add columns to the new dataframe containing relevant data from the shot, passing, and shot percentage dataframes
    group_by_season.loc[:, 'SCA90'] = list(df_shot['SCA90'])
    group_by_season.loc[:, 'PassCompletion'] = list(df_pass['Total.Cmp%'])
    group_by_season.loc[:, 'SoT%'] = list(df_shot_percentage['Standard.SoT%'])
    
    # return the new dataframe
    return group_by_season# Import the necessary packages and libraries

def shot_percentage_stats(player_name):
    """Get the shot percentage statistics for a given player.

    Args:
        player_name (str): The name of the player.

    Returns:
        pandas.DataFrame: The shot percentage statistics for the player.
    """
    
    # Load the shot percentage data for the player
    df_shot_percentage = pd.read_csv(DATASETS_PATH + player_name + '/shot.csv')
    
    # Format the dataframe
    df_shot_percentage = utils.format_dataframe(df_shot_percentage)
    
    # Select the columns we're interested in
    df_shot_percentage = df_shot_percentage.loc[:, ["Season", "Standard.SoT%"]]
    
    # Return the resulting dataframe
    return df_shot_percentage

# Define a function to standardize the player's performance data
def standarize_df(df, max_goal_ratio, max_assist_ratio, max_sca, max_pass, max_sot):
    """Standardize the player's performance data.

    Args:
        df (pandas.DataFrame): The player's performance data.
        max_goal_ratio (float): The maximum goal ratio.
        max_assist_ratio (float): The maximum assist ratio.
        max_sca (float): The maximum SCA.
        max_pass (float): The maximum pass completion percentage.
        max_sot (float): The maximum shot on target percentage.

    Returns:
        pandas.DataFrame: The standardized performance data.
    """
    
    # Standardize the columns of interest using .loc accessor
    df.loc[:, 'Par90minutes.Buts'] = df['Par90minutes.Buts'] / max_goal_ratio
    df.loc[:, 'Par90minutes.PD'] = df['Par90minutes.PD'] / max_assist_ratio
    df.loc[:, 'SCA90'] = df['SCA90'] / max_sca
    df.loc[:, 'PassCompletion'] = df['PassCompletion'] / max_pass
    df.loc[:, 'SoT%'] = df['SoT%'] / max_sot
    
    # Return the standardized dataframe
    return df

# Define a function to adjust the player's performance data
def adjust_players_performance_data(name, df):
    """Adjust the player's performance data.

    Args:
        name (str): The name of the player.
        df (pandas.DataFrame): The player's performance data.

    Returns:
        dict: The adjusted performance data.
    """
    
    # Iterate through the rows of the dataframe and reformat the data
    values = []
    for i, row in df.iterrows():
        year = int(i+1)
        data = [row['Par90minutes.Buts'], row['Par90minutes.PD'], row['SCA90'], row['PassCompletion'], row['SoT%'], row['Par90minutes.Buts']]
        values.append({'year': year, 'data': data})
    
    # Return the adjusted data as a dictionary
    return {'name': name, 'values': values}

def get_players_statistics():
    """
    This function processes data related to goal, shot, pass, shot percentage and goal/assist statistics for football players
    and returns standardized and adjusted data for visualization.

    Returns:
        list: A list of pandas dataframes containing standardized and adjusted data for each player
    """
    # Get goal/assist statistics for each player
    players = ['cristiano', 'rashford', 'messi', 'suarez', 'costa']
    goal_ass_stats_list = []
    for player in players:
        stats = goal_ass_stats(player)
        if player == 'cristiano':
            stats = stats.drop([23]) # Remove seasons with Alnassr
        goal_ass_stats_list.append(stats)

    # Get shot statistics for each player
    shot_stats_list = []
    for player in players:
        stats = shot_stats(player)
        if player == 'cristiano':
            stats = stats.drop([19, 22]) # Remove seasons with Alnassr
        shot_stats_list.append(stats)

    # Get pass statistics for each player
    pass_stats_list = []
    for player in players:
        stats = pass_stats(player)
        if player == 'cristiano':
            stats = stats.drop([19, 23]) # Remove seasons with Alnassr
        pass_stats_list.append(stats)

    # Get shot percentage statistics for each player
    shot_percentage_stats_list = []
    for player in players:
        stats = shot_percentage_stats(player)
        if player == 'cristiano':
            stats = stats.drop([20, 22]) # Remove seasons with Alnassr
        shot_percentage_stats_list.append(stats)

    # Get last 5 years of statistics for each player
    last_5_years_list = []
    for i in range(len(players)):
        last_5_years = group_last_5_years_data(shot_stats_list[i], pass_stats_list[i], shot_percentage_stats_list[i], goal_ass_stats_list[i])
        last_5_years.drop('Saison', axis=1, inplace=True)
        last_5_years = last_5_years.astype(float)
        last_5_years_list.append(last_5_years)

    # Standardize the data for each player
    max_values_list = []
    for player in last_5_years_list:
        max_values = player.apply(max, axis=0)
        max_values_list.append(max_values)

    concatenated_max_values = pd.concat(max_values_list, axis=1)
    max_goal_ratio, max_assist_ratio, max_sca, max_pass, max_sot = concatenated_max_values.iloc[0:].max(axis=1)

    standardized_data_list = []
    for i in range(len(players)):
        player_data = last_5_years_list[i]
        max_values = max_values_list[i]
        standardized_data = standarize_df(player_data, max_goal_ratio, max_assist_ratio, max_sca, max_pass, max_sot)
        standardized_data_list.append(standardized_data)

    # Adjust player names in the data
    players_list = ['Cristiano Ronaldo', 'Marcus Rashford', 'Lionel Messi', 'Luis Suarez', 'Diego Costa']
    adjusted_data_list = []
    for i in range(len(players)):
        adjusted_data = adjust_players_performance_data(players_list[i], standardized_data_list[i])
        adjusted_data_list.append(adjusted_data)

    return adjusted_data_list
