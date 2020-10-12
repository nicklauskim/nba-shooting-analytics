#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nicklauskim
"""


from stat_scraper import scrape_data


# Set desired parameters
season = 2020
stat_type = 'advanced'


# Call scraping function
data = scrape_data(season, stat_type)


# Output file
file_name = 'nba_{}_{}.csv'.format(season, stat_type)
data.to_csv(file_name, sep = ',')