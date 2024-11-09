#Get Flask
from flask import Flask, render_template, request, redirect, url_for, session

import secrets
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("homepage.html")
    