# NFL Strength of Schedule Web App
### **Background**
This program is my final project for the CS50 course. It's a web app that uses data received from the 2020 and 2021 seasons to provide a base rating for each team going into the 2022 season. 

Through data received from an API, it processes up-to-date results from the NFL and converts them into a rating that is applied to each team. This rating represents the current strength of a team based on how they have performed in the 2022 season.

### **Set Up**
#### 1. Cloning
First, clone this repository in the directory that you would like to store this project by running: 

```
git clone git@github.com:BBarkworth/final-project.git
```

#### 2. Set up a virtual environment and install Flask
Set up a virtual environment and install Flask by visiting this [site](https://flask.palletsprojects.com/en/2.2.x/installation/#install-flask) and following the instructions.

#### 3. Run Flask
Enter `Flask run` in the command line in the project directory and follow the hyperlink to access a local version of this project.

### **The Rating System**
The rating system utilises an Elo formula that weights the results of a game based on the difference in quality between teams rather than assuming each win is worth the same amount of points. 
Results were scaled by taking the logarithm and normalised so they were between 1 and 5, with 1 being the worst and five being the best.

```math
E_1{=10^{^{\frac{R_{1}}{400}}}}
```
```math
E_2{=10^{^{\frac{R_{2}}{400}}}} 
```
```math
R_{1}^{'} = R_{1} + K(S_{1} - \frac{E_{1}}{E_{1} + E_{2}}) 
```
```math
R_{2}^{'} = R_{2} + K(S_{2} - \frac{E_{2}}{E_{1} + E_{2}}) 
```
for more information: https://elliotchance.medium.com/elo-rating-system-implemented-in-single-sql-select-9511bdff6434

### **Python Functions**
The tools file consists of various functions that are used in the main app file. 
These include:
* `rating_change`: applies the Elo formula to the respective ratings of the teams playing each other
* `rating`: converts the ratings into a range of 1-5 via $log_{10}$ and data normalisation
* `ties`: which is similar to `rating_change` but is used for ties (this was kept separate for the sake of clarity in the main app file)
* `carry_over`: ensures teams retain only 75% of their rating from previous seasons to ensure the ratings are weighted more towards the latest season.

### **Routes**
The teams route provides a choice for the user so they can pick any team from the NFL and it shows the schedule for that team while also providing updated ratings based on the result of the matches.

The scores route provides the schedule for that week and the scores if the games have been played. The ratings are either pre-match if the game is yet to be played or an updated rating based on the result of the match. 		

The preseason route shows the rating for each team going into the season.

### **Minimum Version Requirements**
* Python 3.9
* Sqlite 3.39.3
* Flask 2.2.2

### **Sources**
1. [FiveThirtyEight](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/)
2. [Metin's Media and Math](https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/comment-page-2/)
3. [Pro Football Reference](https://www.pro-football-reference.com/)
