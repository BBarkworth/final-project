import requests
# library for working with APIs
import json 
# library for working with JSON data
import csv
# for reading csv files
import sqlite3
# for working with sqlite - alternative to using CS50 library
# check line 493 exercise on exercises for how to add SQL table
import math
# for log calcs and round down calcs

def test(obj):
    text = json.dumps(obj, indent=4)
    print(text)
    # sorts data and indents so it's readable

#response = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams")
#print(response.status_code)

# print(response.json())

#teams_response = requests.get("https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32")
    # use teams csv instead??


scores = {}
start = 1500
# initial value 
with open('nfl_teams.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
            scores[row[1]] = start
# NFL teams list for SQL

def rating(func_dict):
    log_dict = {}
    for key, value in func_dict.items():
        log_num = math.log10(value)
        log_dict[key] = log_num
    test_dict = {}
    team_list = []
    max_num = 0
    min_num = 0
    counter = 0
    for key, value in log_dict.items():
        if value > max_num:
            max_num = value
        if counter < 1:
            min_num = value
        if min_num > value:
            min_num = value
        counter += 1
    for key, value in log_dict.items():
        new_max = 5
        new_min = 1 
        new_value = (new_max - new_min) / (max_num - min_num) * (value - max_num) + 5
        new_value = round(new_value)
        test_dict[key] = new_value
    return(test_dict, log_dict)
    # function to convert the data from large values to rating out of 5 via log10 and data re_scaling

def rating_change(winner, loser):
    K_factor = 75
    l = 10 ** (winner/400)
    r = 10 ** (loser/400)
    l2 = l / (l+r)
    r2 = r / (l+r)
    lfinal = round(winner + K_factor*(1-l2))
    rfinal = round(loser + K_factor*(0-r2))
    return(lfinal, rfinal)
# function to work out rating change for each match 

def ties(team1, team2):
    K_factor = 75
    t1 = 10 ** (team1/400)
    t2 = 10 ** (team2/400)
    t1divide = t1 / (t1+t2)
    t2divide = t2 / (t1+t2)
    team1final = round(team1 + K_factor*(0.5-t1divide))
    team2final = round(team2 + K_factor*(0.5-t2divide))
    return(team1final, team2final)

def carry_over(rating):
    new_rating = (0.75 * rating) + (0.25 * 1500)
    return new_rating

with open('2020fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
        if row[5] == row[6] and row[3] == '@':
            temp_rating = scores[row[4]] + 100
            update = ties(scores[row[2]], temp_rating)
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
        elif row[5] == row[6] and row[3] != '@':
            temp_rating = scores[row[2]] + 100
            update = ties(temp_rating, scores[row[4]])
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
        elif row[3] == '@':
            temp_rating = scores[row[4]] + 100
            update = rating_change(scores[row[2]], temp_rating)
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
        else:
            temp_rating = scores[row[2]] + 100
            update = rating_change(temp_rating, scores[row[4]])
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
        # temp_rating includes 100 to take into account home field advantage
# NFL 2020 regular and playoff season results for ranking calc + then SQL insert

for key, value in scores.items():
    change = carry_over(value)
    scores.update({key:change})
    # 2020 carry_over

with open('2021fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
        if row[5] == row[6] and row[3] == '@':
            temp_rating = scores[row[4]] + 100
            update = ties(scores[row[2]], temp_rating)
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
        elif row[5] == row[6] and row[3] != '@':
            temp_rating = scores[row[2]] + 100
            update = ties(temp_rating, scores[row[4]])
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
        elif row[3] == '@':
            temp_rating = scores[row[4]] + 100
            update = rating_change(scores[row[2]], temp_rating)
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
        else:
            temp_rating = scores[row[2]] + 100
            update = rating_change(temp_rating, scores[row[4]])
            scores.update({row[2]:update[0]})
            scores.update({row[4]:update[1]})
# NFL 2021 regular and playoff season results for ranking calc + then SQL insert

for key, value in scores.items():
    change = carry_over(value)
    scores.update({key:change})
    # 2021 carry_over

# break here or move 2022 data for the scores page - see note at the bottom about SQL

with open('2022fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
        if int(row[0]) < 10:
            if row[6] == row[7] and row[4] == '@':
                temp_rating = scores[row[5]] + 100
                update = ties(scores[row[3]], temp_rating)
                scores.update({row[3]:update[0]})
                scores.update({row[5]:update[1]})
            elif row[6] == row[7] and row[4] != '@':
                temp_rating = scores[row[3]] + 100
                update = ties(temp_rating, scores[row[5]])
                scores.update({row[3]:update[0]})
                scores.update({row[5]:update[1]})
            elif row[4] == '@':
                temp_rating = scores[row[5]] + 100
                update = rating_change(scores[row[3]], temp_rating)
                scores.update({row[3]:update[0]})
                scores.update({row[5]:update[1]})
            else:
                temp_rating = scores[row[3]] + 100
                update = rating_change(temp_rating, scores[row[5]])
                scores.update({row[3]:update[0]})
                scores.update({row[5]:update[1]})
        else:
            break
# 2022 schedule

print(rating(scores))

    
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
# add into SQL with team strength rating after 2021 results
    # this SQL column can then be updated after each fixture