#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:01:53 2020

@author: nicklauskim
"""


# Import libraries
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


# Set the desired season and stat type and create the correct basketball-reference.com url to search through
season = 2020
stat_type = 'per_game'
url = 'https://www.basketball-reference.com/leagues/NBA_{}_{}.html'.format(season, stat_type)

# Create soup object for parsing through the html
html = urlopen(url)
soup = BeautifulSoup(html, features = 'lxml')


#print(soup.findAll('tr', limit = 1))

# Get all of the column headers from the table (e.g., Player, Pos, Age, etc.)
col_headers = [th.getText() for th in soup.findAll('tr', limit = 1)[0].find_all('th')]
# Remove the 'Rank' header
col_headers = col_headers[1:]


# Exclude the first row, the headers row
rows = soup.findAll('tr')[1:]
# Make 2-dimensional list to contain table contents
player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]


# Create pandas DataFrame from our 2-D list of player stats
stats = pd.DataFrame(player_stats, columns = col_headers)


# Delete empty/blank rows
stats.dropna(axis = 0, how = 'all', inplace = True)


# Output file
file_name = 'nba_{}_stats_{}.csv'.format(stat_type, season)
stats.to_csv(file_name, sep = ',')


