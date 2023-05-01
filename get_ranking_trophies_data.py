"""the file contain two functions that load and clean up data related to Cristiano Ronaldo's club rankings and trophies"""

import pandas as pd
from utils import get_data_from_file
CLUB_RANKING_FILEPATH ="./datasets/cristiano/club_ranking.xlsx"
LIGUE_FILEPATH = "./datasets/cristiano/ligues_nat.xlsx" 
NATIONAl_COMP_FILEPATH = "./datasets/cristiano/coupes_nat.xlsx" 
INTERNATIONAL_COMP_FILEPATH = "./datasets/cristiano/coupes_inter.xlsx"


def get_ranking_data():
    """
    Load and clean up the CR7 club ranking data.
    Returns:
        ranking_df (pandas.DataFrame): Dataframe with club rankings by season.
    """
    # Load raw data
    raw_data = get_data_from_file(CLUB_RANKING_FILEPATH) 
    
    # Filter data
    filtered_data = raw_data.filter(['Saison','Équipe', 'CltChamp'], axis=1)
    
    # Convert Ranking to numerical values
    mapping = {'1er': 1, '2e': 2, '3e': 3, '4e': 4, '5e': 5, '6e': 6}
    numerical_rank = filtered_data.replace({'CltChamp': mapping})
    
    # Grouping data by teams
    ranking_df = pd.pivot_table(numerical_rank, index='Saison', columns='Équipe', values='CltChamp')
    
    # Add Column of the current team
    ranking_df['Team'] = ranking_df.idxmax(axis=1)
    
    return ranking_df


def get_trophies_data():
    """
    Load and clean up the CR7 trophies data.
    Returns:
        trophies_df (pandas.DataFrame): Dataframe with number of trophies won by CR7 and his teams.
    """
    # Load raw data
    ligue_data = get_data_from_file(LIGUE_FILEPATH) 
    coup_nat_data = get_data_from_file(NATIONAl_COMP_FILEPATH) 
    coup_inter_data = get_data_from_file(INTERNATIONAL_COMP_FILEPATH) 
    
    # Get the season, team name, competition, and ranking
    filtered_ligue_data = ligue_data.filter(['Saison','Équipe', 'Comp', 'CltChamp'], axis=1)
    filtered_coup_nat_data = coup_nat_data.filter(['Saison','Équipe', 'Comp', 'CltChamp'], axis=1).fillna(0)
    filtered_coup_inter_data = coup_inter_data.filter(['Saison','Équipe', 'Comp', 'CltChamp'], axis=1)
    
    # Merge all competition categories
    merged_df = pd.merge(pd.merge(filtered_ligue_data, filtered_coup_nat_data, how="outer"), filtered_coup_inter_data, how="outer")
    
    # Replace "W" or "1er" with 1 and others with 0 in the specified columns
    merged_df[['CltChamp']] = merged_df[['CltChamp']].replace(['W', '1er'], 1)
    merged_df[['CltChamp']] = merged_df[['CltChamp']].replace(to_replace=r'\b(?!1\b)(?!W\b)\w+\b', value=0, regex=True)
    
    # Filter the rows where CltChamp = 1, group by Saison and aggregate the Comp names
    trophies_df = merged_df[merged_df['CltChamp'] == 1].groupby(['Saison','Équipe'])['Comp'].agg(list)
    
    # Reset the index and rename the additional column
    trophies_df = trophies_df.reset_index().rename(columns={'value': 'Comp'})
    
    # Count trophies for each season
    trophies_df['Comp_count'] = trophies_df['Comp'].apply(lambda x: len(x))

    return trophies_df