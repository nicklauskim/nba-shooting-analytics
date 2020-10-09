#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:01:53 2020

@author: nicklauskim
"""


# Import libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd


season = 2020
stat_type = 'shooting'

# Define function to scrape data from basketball-reference.com according to season + stat type
#def scrape_data(season = 2020, stat_type = 'per_game'):
'''

Parameters
----------
season : TYPE, optional
    DESCRIPTION. The default is 2020.
stat_type : TYPE, optional
    DESCRIPTION. The default is 'per_game'.

Returns
-------
None.

'''

# Set the desired season and stat type and create the correct basketball-reference.com url to search through
url = 'https://www.basketball-reference.com/leagues/NBA_{}_{}.html'.format(season, stat_type)


# Create soup object for parsing through the html
html = urlopen(url)
soup = BeautifulSoup(html, features = 'lxml')


# Get all column over-headers (e.g., Dunks, Corner 3s, Heaves) and headers (Player, Pos, Age, etc.) from the table
col_over_headers = [th.getText() for th in soup.findAll('tr', limit = 1)[0].find_all('th')]
col_headers = [th.getText() for th in soup.findAll('tr', limit = 2)[1].find_all('th')]
# Remove the 'Rank' header
col_over_headers = col_over_headers[1:]
col_headers = col_headers[1:]
# Drop all of the empty strings from list of over-headers so we're left with just the actual over_header names
col_over_headers = list(filter(lambda x: (x != '' and x != '\xa0'), col_over_headers))    # \xa0 is non-breaking space


if stat_type == 'shooting':
    # Create multi-column index for the data so all column indices are unique (better way to do this?)
    no_over_header = [('', header) for header in col_headers[0:8]]
    percent_of_fga_by_dist = [(col_over_headers[0], header) for header in col_headers[9:15]]
    fg_percentage_by_dist = [(col_over_headers[1], header) for header in col_headers[16:22]]
    percent_of_fga_astd = [(col_over_headers[2], header) for header in col_headers[23:25]]
    dunks = [(col_over_headers[3], header) for header in col_headers[26:28]]
    corner_3s = [(col_over_headers[4], header) for header in col_headers[29:31]]
    heaves = [(col_over_headers[5], header) for header in col_headers[32:34]]
    
    list_of_multiindex_tuples = no_over_header + percent_of_fga_by_dist + fg_percentage_by_dist + percent_of_fga_astd + dunks + corner_3s + heaves
    col_headers = pd.MultiIndex.from_tuples(list_of_multiindex_tuples)

    
else:
    pass
    


# Exclude the first row, the headers row
rows = soup.findAll('tr')[2:]

# Make 2-dimensional list to contain table contents
player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

# Create pandas DataFrame from our 2-D list of player stats
stats = pd.DataFrame(player_stats)

# Replace empty strings/entries with np.nan to flag them as missing values
stats.replace('', np.nan, inplace = True)


# Delete empty/blank rows and columns
stats.dropna(axis = 0, how = 'all', inplace = True)
stats.dropna(axis = 1, how = 'all', inplace = True)


stats.columns = col_headers


# Output file
#file_name = 'nba_{}_stats_{}.csv'.format(stat_type, season)
#stats.to_csv(file_name, sep = ',', index_col = 'Player')


