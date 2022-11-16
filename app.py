import os

from flask import Flask, redirect, render_template, request, session
from flask_session.__init__ import Session

from tools import rating, rating_change, ties, carry_over

import sqlite3
# for working with sqlite - alternative to using CS50 library
import csv
# for reading csv files

app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect('nflteamsdb.sqlite', check_same_thread=False)

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Teams')

cur.execute('DROP TABLE IF EXISTS Fixtures')

cur.execute('''
CREATE TABLE Teams (id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, abbreviation TEXT NOT NULL, conference TEXT NOT NULL, division TEXT NOT NULL, rating INTEGER)''')

cur.execute('''
CREATE TABLE Fixtures (fixture_id INTEGER PRIMARY KEY NOT NULL, week TEXT NOT NULL, ratingone INTEGER, teamone TEXT NOT NULL, at TEXT, teamtwo TEXT NOT NULL, ratingtwo INTEGER)''') 

scores = {}
start = 1500
# initial value 
with open('nfl_teams.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    for row in reader:
        scores[row[1]] = start
        team_name = row[1]
        abbr = row[2]
        conf = row[3]
        div = row[4]
        cur.execute('''INSERT INTO Teams (name, abbreviation, conference, division, rating) VALUES (?,?,?,?,?)''', (team_name, abbr, conf, div, start))
    conn.commit()
# NFL teams list for SQL

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

pre_season_ratings = rating(scores)
# break here or move 2022 data for the scores page - see note at the bottom about SQL

for key, value in pre_season_ratings.items():
    cur.execute('''UPDATE Teams SET rating = ? WHERE name = ?''', (value, key))
conn.commit

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

'''
options = cur.execute('SELECT name, rating FROM Teams ORDER BY name').fetchall()
print(options)
for option in options:
    print("OPTIONS: ", option)
test_list = []
for row in cur.execute('SELECT name,rating FROM Teams ORDER BY name').fetchall():
    test_list.append(row)
print("TEST LIST: ", test_list)
''' 
# Jinja templating tests

#print(rating(scores))

with open('2022fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    # skip header
    next(reader)
    # split week and fixtures into separate columns
    for row in reader:
        week = row[0]
        team_one = row[3]
        home_or_away = row[4]
        team_two = row[5]
        cur.execute('''INSERT INTO Fixtures (week, teamone, at, teamtwo) VALUES (?,?,?,?)''', (week, team_one, home_or_away, team_two))
        cur.execute('''UPDATE Fixtures set ratingone = (SELECT rating FROM Teams WHERE name = ?)''', (team_one,))
        cur.execute('''UPDATE Fixtures set ratingtwo = (SELECT rating FROM Teams WHERE name = ?)''', (team_two,))
    conn.commit()

@app.route("/")
def home():
    return render_template("home.html")

'''
@app.route("/scores", methods= ["GET", "POST"])
def scores():
    if request.method == "GET":
        return render_template("scores.html")

    else:
'''

@app.route("/teams", methods= ["GET", "POST"])
def teams():
    if request.method == "GET":
        test_list = []
        for row in cur.execute('SELECT name FROM Teams ORDER BY name').fetchall():
            test_list.append(row)
        return render_template("choices.html", test_list = test_list)
    else:
        choice = request.form.get("t")
        # include apology page with error + message
        fixture_data = cur.execute('''SELECT week, ratingone, teamone, at, teamtwo, ratingtwo FROM Fixtures WHERE teamone = ? OR teamtwo = ?''', (choice, choice))
        return render_template("schedule.html", fixture_data = fixture_data, choice = choice)