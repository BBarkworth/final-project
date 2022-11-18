# final-project
CS50 final project

win values set as 100 for regular season and 200 for playoffs. This is to give some additional value to the playoff games and provide a significant gap between the top teams and the rest, while also avoiding any odd number issues related to high regular season totals versus lower regular season totals and higher playoff totals when two teams are compared
The data was then log10ed to reduce the gaps between the data and then equal dividers were placed between the data to group it
For the ELO formula, the K rating was set as 300 as it's a good arbitrary value for the dataset because it ensures there's plenty of movement
https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/
# needs reworking + add sources

Had issues with Sqlite return structures - initially accessed data as a tuple but ultimately reworked it by using Sqlite dict cursor as I'm more comfortable accessing SQL data in that way.
POST function for /Teams decorator was reworked so the INSERT and UPDATE SQL queries were completed outside of it when accessing a CSV, this allowed it to be much cleaner as it required less conditionals  - this was combined with rewriting a CSV file so the conditionals could be reduced as the data was structured in a better way

Bootstrap was used on the frontend to make the site look as clean as possible and a table was ultimately used as the way to show data from the initial GET query on the /Teams decorator as it presented the data in the best way - little areas such as the size of the text, wrapping and size restrictions were used to make it look as clean as possible. 