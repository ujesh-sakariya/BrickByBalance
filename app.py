#Get Flask
from flask import Flask, render_template, request, redirect, url_for, session

import secrets
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("homepage.html")

# handles the mortgage calculator route 
@app.route('/mortgageCalculator',methods=["GET","POST"])
def mortgageCalculator():

    if request.method == 'GET':
        # return the page 
        return render_template('mortgageCalculator.html')

