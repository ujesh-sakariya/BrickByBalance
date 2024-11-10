#Get Flask
from flask import Flask, render_template, request, redirect, url_for, session

import secrets
app = Flask(__name__)

import threading


app.secret_key = secrets.token_hex(16)

# get the DB
import sqlite3

def getConnection():
    connection = sqlite3.connect('BrickByBalance.db')
    return connection  

def removeConnection(connection):
    connection.close()
    return



@app.route("/")
def index():
    return render_template("homepage.html")

# handles the mortgage calculator route 
def mortgageCalculator():

    if request.method == 'GET':
        # return the page 
        return render_template('mortgageCalculator.html')
    
# handle routes for login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method =="POST":

        # Obtains the username and password from the data that is posted
        username = request.form.get('username')      
        password = request.form.get('password')

        # Query to check if an account exists with the given username and password
        query = "SELECT username, password, email FROM accounts WHERE username = ? AND password = ?"
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(query, (username, password))
        acc = cursor.fetchone()
        if acc == None:
            # Output error message 
            removeConnection(connection)
            return render_template('login.html',fail = 'Incorrect username or password')
        else:

            # set the session to the current user 
            session["name"] = username
            removeConnection(connection)
            return render_template("homepage.html")
    else:
        # direct user to the login page 
        return render_template('login.html')

# handle routes for registraton
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method =="POST":

        #get the data from register
        username = request.form.get('username')      
        password = request.form.get('password')
        email = request.form.get('email')
        data = [username]

        #check if an account exists with the given username 
        query = "SELECT username FROM accounts WHERE username = ?"
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(query,(data))
        status = cursor.fetchone()
        if status != None:
            # Output error message 
            return render_template('register.html', fail = 'username is already taken')

        # set the session to the current user 
        session["name"] = username
        
        add_accounts = "INSERT INTO accounts (username, password, email) VALUES (?, ?, ?)"
        data_accounts = (username,password,email)
        #inserting data 
        cursor.execute(add_accounts, data_accounts)
        #commit to db
        connection.commit()
        removeConnection(connection)
        return render_template('homepage.html')
    else:
        # GET METHOD
        return render_template('register.html')
    
# clear the session and takeuser back the homepage
@app.route("/logout")
def logout():
    session.clear()
    return render_template('homepage.html')

@app.route('/prediction',methods=['GET','POST'])
def prediction():
    if request.method == 'POST':
        houseType = request.form.get('houseType')
        years = request.get.form('years')
        savings = request.get.form('savings')
        region = request.get.form('region')
    else:
        return render_template('prediction.html')



    
