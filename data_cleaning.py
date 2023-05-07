#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:17:19 2020

@author: nicklauskim
"""


import pandas as pd


filepath = './nba_2020_shooting_stats.csv'
df = pd.read_csv(filepath, header = [0, 1], index_col = 0)


# Fix column names
df.columns = [c for _, c in df.columns[:8]] + [c for c in df.columns[8:]]
df = df.set_index(list(df.columns[:8]), append = True)
df.columns = pd.MultiIndex.from_tuples(df.columns)

df.reset_index(col_level = 1, inplace = True)

# Get rid of unwanted extra column
df.drop(('', 'level_0'), axis = 1, inplace = True)


# Check data types of columns
#print(df.dtypes)





# Different ways to index by column(s)
#idx = pd.IndexSlice
#df.loc[:, idx['', :]]

#df.loc[:, (slice(None), 'Player')]

#df.xs('Dunks', axis = 1)





# Save file
#df.to_csv(filepath)