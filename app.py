# remember virtual environment for this project is called projectenv
# use conda activate projectenv to activate it
import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session.__init__ import Session

app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



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
'''
@app.route("/teams", methods= ["GET", "POST"])
def teams():
    if request.method == "GET":
        return render_template("choices.html")

    else:
    # complete /post code for this route - lists schedule for team chosen
        # with team strength next to each team
'''