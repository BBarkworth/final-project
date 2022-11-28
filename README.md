# NFL Strength of Schedule Web App
### **Video Demo:**  https://youtu.be/1c_zrWY-PSY
### **Description:**
This program is my final project for the CS50 course. It's an NFL strength of schedule web app which uses data from the 2020 and 2021 seasons to provide a base rating for each team going into the 2022 season and then it updates dynamically based on real-world results. Through data received from CSVs and an API, it processes results from the NFL and converts them via various functions into a rating between 1 and 5 that is applied to each team. This represents the current strength of the team based on the results that have come before.

The app is mainly written in Python and utilises the Flask framework, but it also includes SQL to handle storing the data and database queries, HTML for the front end, and Jinja for passing data between Python and HTML. I also opted to use Bootstrap for the front end to make the web app look as professional and clean as possible. I used Flask as I'm familiar with using Jinja to pass data from Python to HTML and I knew that would be a crucial part of this project. 

### **The Rating System**
The rating system utilises an Elo formula which takes into consideration the gulf in quality between two teams rather than assuming each win is worth the same amount of points. This is a way to potentially indicate whether a team is improving or declining. I opted for a K factor of 75 in the formula to ensure the ratings were relatively fluid. These two links [FiveThirtyEight] (https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/) and [Metin's Media and Math] (https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/comment-page-2/) were used as sources for how best to implement an Elo system. Results were scaled by taking the logarithm and normalised so they were between 1 and 5, with 1 being the worst and five being the best. 

### **Data Source**
The data for the two previous seasons was taken from [Pro Football Reference] (https://www.pro-football-reference.com/) as CSV files. An API provides the current season's data so that it can stay up-to-date without requiring manual input, although there is a CSV file included that acts as a backup in case the API doesn't return anything or revokes access.

### **Python Files**
The tools file consists of various functions that are used in the main app file. 
These include:
* `rating_change`: applies the Elo formula to the respective ratings of the teams playing each other
* `rating`: converts the ratings into a range of 1-5 via log10 and data normalisation
* `ties`: which is similar to `rating_change` but is used for ties (this was kept separate for the sake of clarity in the main app file)
* `carry_over`: ensures teams retain only 75% of their rating from previous seasons to ensure the ratings are weighted more towards the latest season

The CSV formatting file is an example of some code I used to rewrite the CSV files as I cut down the number of conditional checks by ensuring the home team was first in the files. 

The app file consists of a SQL script to drop and create tables whenever the program is run and then reads through a CSV file to insert all the NFL teams into the table with the relevant information. After that, the program processes a 2020 fixtures CSV file where it applies the ties and rating change functions based on the result. The temp rating represents home advantage so that value is used in the rating change function but the actual rating change difference for the home team is worked out from how much the away team rating changed and the scores dictionary that stores the data is updated with that value. The carry-over function is used on the total ratings for that season and the same process is repeated for the 2021 season.

The Teams SQL table is updated with each team's normalised rating going into the 2022 season and the Fixtures SQL table is updated via a CSV with the scores set to 0 by default. Next, a connection is made with an API and the relevant information is retrieved so that it can be compared with the same processes used for the 2020 and 2021 result CSVs. These rating changes are then applied to a copy of the scores dictionary and used to update the SQL table.

### **Routes**
The home route provides a standard homepage template with a basic introduction explaining what the site is. The teams route provides a choice for the user so they can pick any team from the NFL and it shows the schedule for that team while also providing updated ratings based on the result of the matches so you can see how a team's rating has changed throughout the season.

The scores route provides a choice of weeks for the user to select and once selected, they are provided with the schedule for that week and the scores if the games have been played. The ratings are either pre-match if the game is yet to be played or an updated rating based on the result of the match. There is also a html form so the user can move to another week via manual input as having a dropdown form here caused SQL issues due to multiple SQL queries within the same method, but there are various conditional checks in place to avoid user input problems. Finally, the preseason route shows the rating for each team going into the season so the user has something to compare the rating changes throughout the season with.

### **HTML Pages**
The HTML pages were designed using the Bootstrap framework.

### **Mimimum Version Requirements**
* Python 3.10.6
* Sqlite 3.39.3