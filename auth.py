# Blueprint (auth)
# Views Related to Authorisations e.g. login, sign-up, logout

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # imported from init.py file
from flask_login import login_user, login_required, logout_user, current_user # pulls through the current user using user mixin in the models.py file for USER


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST']) # Methods includes which types of requests the routes can recieve.
def login():
   if request.method == 'POST':

      # section used for coding to help understand interfaces
      data = request.form # whenever the request variable is accessed inside the route it will have information about the request that was sent to access this route e.g. the url / method / all information that was sent
      print(data)

      # store the form requests in variables
      email = request.form.get('email')
      password = request.form.get('password')
      # query the database on email and store the user if it exists in user variable
      user = User.query.filter_by(email=email).first()
      # authetication
      if user:
         if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True) # logs the user in using flask_login and remembers logged in on browser
            return redirect(url_for('views.home'))
         else:
            flash('Incorrect password, try again.', category='error')
      else:
         flash('Email does not exist.', category='error')
         
   elif request.method == 'GET':
      return render_template("login.html", boolean=True)

@auth.route('/logout') 
@login_required # only accessible if user is logged in
def logout():
   logout_user() # logs user out using flask_login module
   return redirect(url_for('app.homepage'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
   # Enter the method if there is a post request e.g. someone submits the form
   if request.method == 'POST':     

      # Retrieves information from sign up form
      first_name = request.form.get('firstName')
      last_name = request.form.get('lastName')
      email = request.form.get('email')
      password1 = request.form.get('password1')
      password2 = request.form.get('password2')

      # query the database on email and store the user if it exists in user variable
      user = User.query.filter_by(email=email).first()
      #Validations
      if user:
         flash('Email already exists', category='error')
      elif len(email) < 4:
         flash('Email must be greater than 4 characters', category='error')
      elif len(first_name) < 2:
         flash('First name must be greater than 2 characters', category='error')
      elif password1 != password2:
         flash('Passwords dont match', category='error')
      elif len(password1) < 7:
         flash('Password must be at least 7 characters', category='error')
      else:
         # Add user to Database
         # Create new user using class in the models database and add
         # The left first_name references the User first name column in the database. 
         # The right first_name references the variable pulled in above from the POST method above.
         new_user = User(first_name=first_name, 
                         last_name=last_name, 
                         email=email, 
                         password = generate_password_hash(password1, method='pbkdf2'))
         db.session.add(new_user)
         db.session.commit()
         login_user(new_user, remember=True)
         flash('Account created!', category='success')
         return redirect(url_for('app.homepage'))
   return  render_template("sign_up.html", user=current_user)
