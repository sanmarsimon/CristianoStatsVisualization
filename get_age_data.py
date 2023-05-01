import pandas as pd
import utils

CRISTIANO_STATS_PATHFILE = "./datasets/cristiano/stats.csv"
def get_data():
    """
    Load data from a CSV file and clean it up for visualization 1.
    Returns:
        group_by_age (pandas.DataFrame): Dataframe with age, total goals, and goals per game.
    """
    # Load data and select only relevant columns
    df = pd.read_csv(CRISTIANO_STATS_PATHFILE)
    
    # Rename columns with proper titles
    for title in df.columns:
        if title.startswith("Unnamed"):
            df.rename(columns={title: df.loc[0,title]}, inplace=True)
        else:
            head_title = utils.extract_title(title)
            df.rename(columns={title: head_title  + '.' + str(df.loc[0,title])}, inplace=True)
    df = df.drop([0])
    df.rename(columns={'Âge': 'Age'}, inplace=True)
    df.rename(columns={'Performance.Buts': 'Buts'}, inplace=True)
    
    # Select relevant columns and convert data types
    goal_stats = df[['Age', 'MJ', 'Buts']]
    goal_stats = goal_stats.astype({'Age': int, 'MJ': int, 'Buts': int})
    
    # Group by age and calculate total goals and goals per game
    group_by_age = goal_stats.groupby(['Age']).sum().reset_index()
    group_by_age.loc[:,'Goals per game'] = group_by_age.loc[:,'Buts'] / group_by_age.loc[:,'MJ']
    group_by_age.rename(columns={'Buts': 'Total goals'}, inplace=True)

    # Goals per game is a float, so round it to 2 decimal places
    group_by_age.loc[:, 'Goals per game'] = group_by_age.loc[:,'Goals per game'].astype(float).round(2)
    
    # Return cleaned-up data
    return group_by_age
