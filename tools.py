import requests
# library for working with APIs
import json 
# library for working with JSON data
import csv
# for reading csv files
import sqlite3
# for working with sqlite - alternative to using CS50 library
# check line 493 exercise on exercises for how to add SQL table

def test(obj):
    text = json.dumps(obj, indent=4)
    print(text)
    # sorts data and indents so it's readable

#response = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams")
#print(response.status_code)

# print(response.json())

#teams_response = requests.get("https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32")
    # use teams csv instead??

with open('2022fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
        if row[3] == 'Los Angeles Rams':
            print(row[5])
        if row[5] == 'Los Angeles Rams':
            print(row[3])
# 2022 schedule

with open('nfl_teams.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
            print(row)
# NFL teams list for SQL

with open('NFL.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
            print(row)
# NFL 2021 regular season records for ranking calc + then SQL insert

with open('Playoffs.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
            print(row)

'''
file_name = input("File name: ")
if len(file_name) < 1:
    file_name = "2022fixtures.csv"
handle = open(file_name)
counter = 0
for line in handle:
'''
# file options rather than csv
    
#print(teams_response.status_code)

#print(teams_response.json())

#test(teams_response.json())

#scores_response = requests.get("http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")

#print(scores_response.status_code)

# print(scores_response.json())

# response code indicates whether successful i.e. 200
# data needs to be sorted with a precise request

# https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c
    # https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams
    # https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32
# https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b
    # http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard


# code scoring system
# add into SQL with team strength rating based on last year's results
    # this SQL column can then be updated after each fixture
# use API to load last season's total wins-losses or input manually?
# score playoff wins differently i.e. 150 rather than 100
# rating score will be out of 5 as visual for user but larger behind the scenes

# work out calc then log10 then normalise to scale them