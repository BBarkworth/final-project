from flask import Flask, render_template, request
from flask_session.__init__ import Session
from tools import rating, rating_change, ties, carry_over
import sqlite3
# for working with sqlite - alternative to using CS50 library
import csv
# for reading csv files
import requests
# library for working with APIs
import json 
# library for working with JSON data
import copy
# for copy of pre season ratings

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
# Ensure templates are auto-reloaded
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure session to use filesystem (instead of signed cookies)

conn = sqlite3.connect('nflteamsdb.sqlite', check_same_thread=False)
conn.row_factory = sqlite3.Row
# dict cursor for Sqlite library
cur = conn.cursor()
cur.executescript("""
    DROP TABLE IF EXISTS Teams;
    DROP TABLE IF EXISTS Fixtures;
    CREATE TABLE Teams(id INTEGER PRIMARY KEY NOT NULL, name TEXT NOT NULL, abbreviation TEXT NOT NULL, conference TEXT NOT NULL, division TEXT NOT NULL, rating INTEGER);
    CREATE TABLE Fixtures(fixture_id INTEGER PRIMARY KEY NOT NULL, week TEXT NOT NULL, ratingone INTEGER, teamone TEXT NOT NULL, scoreone INTEGER, scoretwo INTEGER, teamtwo TEXT NOT NULL, ratingtwo INTEGER);
    """)

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
        cur.execute('INSERT INTO Teams (name, abbreviation, conference, division, rating) VALUES (?,?,?,?,?)', (team_name, abbr, conf, div, start))
    conn.commit()
# NFL teams list for SQL

with open('2020fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    next(reader)
    for row in reader:
        if int(row[4]) == int(row[5]):
            temp_rating = scores[row[2]] + 100
            update = ties(temp_rating, scores[row[3]])
            diff = update[1] - scores[row[3]]
            if diff < 0:
                new_value = scores[row[2]] + (diff * -1)
            else:
                new_value = scores[row[2]] - diff
            scores.update({row[2]:new_value, row[3]:update[1]})
        elif int(row[4]) > int(row[5]):
            temp_rating = scores[row[2]] + 100
            update = rating_change(temp_rating, scores[row[3]])
            diff = update[1] - scores[row[3]]
            new_value = scores[row[2]] + (diff * -1)
            scores.update({row[2]:new_value, row[3]:update[1]})
        else:
            temp_rating = scores[row[2]] + 100
            update = rating_change(scores[row[3]], temp_rating)
            diff = update[0] - scores[row[3]]
            new_value = scores[row[2]] - diff
            scores.update({row[2]:new_value, row[3]:update[0]})
        # temp_rating includes 100 to take into account home field advantage - diff is then used to work out how much home team original rating should change
# NFL 2020 regular and playoff season results for ranking calc

for key, value in scores.items():
    change = carry_over(value)
    scores.update({key:change})
    # 2020 carry_over

with open('2021fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    next(reader)
    for row in reader:
        if int(row[4]) == int(row[5]):
            temp_rating = scores[row[2]] + 100
            update = ties(temp_rating, scores[row[3]])
            diff = update[1] - scores[row[3]]
            if diff < 0:
                new_value = scores[row[2]] + (diff * -1)
            else:
                new_value = scores[row[2]] - diff
            scores.update({row[2]:new_value, row[3]:update[1]})
        elif int(row[4]) > int(row[5]):
            temp_rating = scores[row[2]] + 100
            update = rating_change(temp_rating, scores[row[3]])
            diff = update[1] - scores[row[3]]
            new_value = scores[row[2]] + (diff * -1)
            scores.update({row[2]:new_value, row[3]:update[1]})
        else:
            temp_rating = scores[row[2]] + 100
            update = rating_change(scores[row[3]], temp_rating)
            diff = update[0] - scores[row[3]]
            new_value = scores[row[2]] - diff
            scores.update({row[2]:new_value, row[3]:update[0]})
# NFL 2021 regular and playoff season results for ranking calc

for key, value in scores.items():
    change = carry_over(value)
    scores.update({key:change})
    # 2021 carry_over

pre_season_ratings = rating(scores)
for key, value in pre_season_ratings.items():
    cur.execute('UPDATE Teams SET rating = ? WHERE name = ?', (value, key))
    # SQL update for pre-season ratings

with open('2022fixtures.csv', 'r') as in_file:
    reader = csv.reader(in_file)
    next(reader)
    for row in reader:
        week = row[0]
        team_one = row[3]
        team_two = row[4]
        tempscore = 0
        cur.execute('INSERT INTO Fixtures (week, teamone, scoreone, scoretwo, teamtwo) VALUES (?,?,?,?,?)', (week, team_one, tempscore, tempscore, team_two))
    conn.commit()
# NFL 2022 season results

api_ratings = copy.deepcopy(scores)
# copy of scores dict to avoid mutation of original data

for i in range(1, 19):
    parameters= {
        "year" : 2022,
        "type": 2,
        "week": i,
        }
        # defaults to current week if no week is provided
    response = requests.get("http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard", params = parameters, timeout=2.50)
    if response.status_code == 200:
        data = response.text
        parse_json = json.loads(data)
        counter = 0
        for event in parse_json['events']:
            for competition in event['competitions']:
                for competitor in competition['competitors']:
                    counter += 1
                    if counter % 2 != 0:
                        homescore = competitor.get('score')
                        homescore = int(homescore)
                        hometeam = competitor['team'].get('displayName')
                    else:
                        awayscore = competitor.get('score')
                        awayscore = int(awayscore)
                        awayteam = competitor['team'].get('displayName')
                    # teams and scores are taken from API endpoint and saved in variables
                    if counter % 2 == 0:
                        # check to ensure home and away team data is compared correctly
                        if homescore > awayscore:
                            temp_rating = api_ratings[hometeam] + 100
                            change_values = rating_change(temp_rating, api_ratings[awayteam])
                            diff = change_values[1] - api_ratings[awayteam]
                            if diff < 0:
                                new_num = api_ratings[hometeam] + (diff * -1)
                            else:
                                new_num = api_ratings[hometeam] - diff
                            api_ratings.update({hometeam:new_num, awayteam:change_values[1]})
                        elif homescore < awayscore:
                            temp_rating = api_ratings[hometeam] + 100
                            change_values = rating_change(api_ratings[awayteam], temp_rating)
                            diff = change_values[0] - api_ratings[awayteam]
                            if diff < 0:
                                new_num = api_ratings[hometeam] + (diff * -1)
                            else:
                                new_num = api_ratings[hometeam] - diff
                            api_ratings.update({hometeam:new_num, awayteam:change_values[0]})
                        elif homescore == 0 and awayscore == 0:
                            continue
                        # check to avoid future games being processed by rating change function
                        else:
                            temp_rating = api_ratings[hometeam] + 100
                            change_values = ties(temp_rating, api_ratings[awayteam])
                            diff = change_values[1] - api_ratings[awayteam]
                            if diff < 0:
                                new_num = api_ratings[hometeam] + (diff * -1)
                            else:
                                new_num = api_ratings[hometeam] - diff
                            api_ratings.update({hometeam:new_num, awayteam:change_values[1]})
                        cur.execute('UPDATE Fixtures set scoreone = ?, scoretwo = ? WHERE teamone = ? AND teamtwo = ?', (homescore, awayscore, hometeam, awayteam))
                        conn.commit()
                        # scores are compared and processed through rating_change function and scores are updated in SQL
                    else:
                        continue
                    
        api_week_values = rating(api_ratings)
        for key, value in api_week_values.items():
            cur.execute('UPDATE Fixtures set ratingone = ? WHERE teamone = ? AND week = ?', (value, key, i))
            cur.execute('UPDATE Fixtures set ratingtwo = ? WHERE teamtwo = ? AND week = ?', (value, key, i))
        conn.commit()
        # ratings are updated in SQL via api_week_values dictionary
    else:
        with open('2022fixtures.csv', 'r') as in_file:
            reader = csv.reader(in_file)
            next(reader)
            for row in reader:
                if int(row[0]) < 12:
                    if int(row[5]) == int(row[6]):
                        temp_rating = scores[row[3]] + 100
                        update = ties(temp_rating, scores[row[4]])
                        diff = update[1] - scores[row[4]]
                        if diff < 0:
                            new_number = scores[row[3]] + (diff * -1)
                        else:
                            new_number = scores[row[3]] - diff
                        scores.update({row[3]:new_number, row[4]:update[1]})
                    elif int(row[5]) > int(row[6]):
                        temp_rating = scores[row[3]] + 100
                        update = rating_change(temp_rating, scores[row[4]])
                        diff = update[1] - scores[row[4]]
                        new_number = scores[row[3]] + (diff * -1)
                        scores.update({row[3]:new_number, row[4]:update[1]})
                    else:
                        temp_rating = scores[row[3]] + 100
                        update = rating_change(scores[row[4]], temp_rating)
                        diff = update[0] - scores[row[4]]
                        new_number = scores[row[3]] - diff
                        scores.update({row[3]:new_number, row[4]:update[0]})
                else:
                    break
    # 2022 schedule csv which acts as a backup if API doesn't return 200

@app.route("/")
def home():
    return render_template("home.html")
# homepage route

@app.route("/teams", methods= ["GET", "POST"])
def teams():
    if request.method == "GET":
        all_teams = cur.execute('SELECT name FROM Teams ORDER BY name')
        return render_template("choices.html", all_teams = all_teams)
    else:
        choice = request.form.get("team_choice")
        if not choice:
            return render_template("apology.html")
        fixture_data = cur.execute('''SELECT week, ratingone, teamone, teamtwo, ratingtwo FROM Fixtures WHERE teamone = ? OR teamtwo = ?''', (choice, choice))
        return render_template("schedule.html", fixture_data = fixture_data, choice = choice)
# route for selecting a team and providing their season schedule

@app.route("/scores", methods= ["GET", "POST"])
def scores():
    weeks = cur.execute('SELECT DISTINCT week FROM Fixtures')
    if request.method == "GET":
        return render_template("scores.html", weeks = weeks)
    else:
        week_choice = request.form.get("week")
        if not week_choice:
            return render_template("apology.html")
        if week_choice.isnumeric() == False:
            return render_template("apology.html")
        if int(week_choice) > 18 or int(week_choice) < 1:
            return render_template("apology.html")
        week_data = cur.execute('''SELECT ratingone, teamone, scoreone, scoretwo, teamtwo, ratingtwo FROM Fixtures WHERE week = ?''', (week_choice,))
        return render_template("fixtures.html", week_choice = week_choice, week_data = week_data, weeks = weeks)
# route for showing the fixtures for each week along with the scores for any completed games and rating changes based on those results

@app.route("/preseason", methods= ["GET"])
def preseason():
    preseason = cur.execute('SELECT name, rating FROM Teams')
    return render_template("preseason.html", preseason = preseason)
# route for showing preseason ratings for each team