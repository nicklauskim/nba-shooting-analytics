#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nicklauskim
"""


# Import libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd



# Define function to scrape player statistics from basketball-reference.com according to season + stat type
def scrape_data(season = 2020, stat_type = 'per_game'):
    '''
    Parameters
    ----------
    season : int, required
        Year in which desired season ended (format YYYY). Ex.: 2020 for 2019-20 NBA season.
        The default is 2020.
    stat_type : string, required
        Type of statistics. Valid options are: 'totals', 'per-game', 'per_minute', 'per_poss', 'advanced', 'shooting'
        The default is 'per_game'.
    
    Returns
    -------
    Dataframe containing player statistics for the chosen season and statistic type.
    '''
    
    # Set the desired season and stat type and create the correct basketball-reference.com url to search through
    url = 'https://www.basketball-reference.com/leagues/NBA_{}_{}.html'.format(season, stat_type)
    
    
    # Create soup object for parsing through the html
    html = urlopen(url)
    soup = BeautifulSoup(html, features = 'lxml')
    
    
    if stat_type == 'shooting':
        # Get all column "over-headers" (e.g., Dunks, Corner 3s, Heaves) and "under-headers" (2P, 0-3, 3-10, etc.) from the table
        upper_headers = [th.getText() for th in soup.findAll('tr', limit = 1)[0].find_all('th')]
        lower_headers = [th.getText() for th in soup.findAll('tr', limit = 2)[1].find_all('th')]
        # Remove the 'Rank/Rk' headers
        upper_headers = upper_headers[1:]
        lower_headers = lower_headers[1:]
        # Drop all of the empty strings from list of over-headers so we're left with just the actual over_header names
        upper_headers = list(filter(lambda x: (x != '' and x != '\xa0'), upper_headers))    # \xa0 is non-breaking space
        # Create multi-column index for the data so all column indices are unique (better way to do this?)
        multiindex_tuples = []
        multiindex_tuples.extend([('', header) for header in lower_headers[0:8]])
        multiindex_tuples.extend([(upper_headers[0], header) for header in lower_headers[9:15]])
        multiindex_tuples.extend([(upper_headers[1], header) for header in lower_headers[16:22]])
        multiindex_tuples.extend([(upper_headers[2], header) for header in lower_headers[23:25]])
        multiindex_tuples.extend([(upper_headers[3], header) for header in lower_headers[26:28]])
        multiindex_tuples.extend([(upper_headers[4], header) for header in lower_headers[29:31]])
        multiindex_tuples.extend([(upper_headers[5], header) for header in lower_headers[32:34]])
        col_headers = pd.MultiIndex.from_tuples(multiindex_tuples)
        
        # Exclude the first two rows, the headers rows
        rows = soup.findAll('tr')[2:]
        
    else:
        # Get all column headers (Player, Pos, Age, etc.)
        col_headers = [th.getText() for th in soup.findAll('tr', limit = 1)[0].find_all('th')]
        # Remove the 'Rank/Rk' header
        col_headers = col_headers[1:]
        # Drop all of the empty strings from list of headers so we're left with just the actual over_header names
        col_headers = list(filter(lambda x: (x != '' and x != '\xa0'), col_headers))    # \xa0 is non-breaking space
        # Exclude the first row, the headers row
        rows = soup.findAll('tr')[1:]
    
    
    # Make 2-dimensional list to contain table contents
    player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    # Create pandas DataFrame from our 2-D list of player stats
    stats = pd.DataFrame(player_stats)
    
    # Replace empty strings/entries with np.nan to flag them as missing values
    stats.replace('', np.nan, inplace = True)
    
    # Delete empty/blank rows and columns
    stats.dropna(axis = 0, how = 'all', inplace = True)
    stats.index = range(len(stats))    # Reindexing
    stats.dropna(axis = 1, how = 'all', inplace = True)
    
    # Set column names
    stats.columns = col_headers
    
    
    return stats



# Call scraping function
season = 2020
stat_type = 'shooting'
data = scrape_data(season, stat_type) 


# Output file
file_name = './Data/nba_{}_{}.csv'.format(season, stat_type)
data.to_csv(file_name, sep = ',')


    