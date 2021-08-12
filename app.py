"""Login Authentification application."""

from flask import Flask, jsonify, redirect, render_template, request, flash, session
import flask
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserRegistrationForm, UserLoginForm, FeedbackForm
from models import db, connect_db, User, Feedback
from sqlalchemy.exc import IntegrityError
import os
import re

app = Flask(__name__)
uri = os.getenv("DATABASE_URL")  # or other relevant config var
# rest of connection code using the connection string `uri`
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///user_feedback_db').replace("://", "ql://", 1) # defaults to the one on right for dev, left is one you set with heroku addons:create heroku-postgresql:hobby-dev #hobby-dev is exactly as it should be
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '\xda\n\xb4N0|\x15\xb8\x0c"\x17\xd5$\xf1RO') #python3 import random, random.randbytes(n)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#Example View Functions
@app.route('/')
def render_welcome():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def display_registration_form():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data    
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register_new_user(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username is taken, please choose a different one')
            return render_template('registration_form.html', form=form)
        flask.session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{username}')
    else:
        return render_template('registration_form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def display_login_form():
    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        curr_user = User.authenticate_user(username, password)
        if curr_user:
            flask.session['username'] = curr_user.username
            flash(f"Welcome Back, {curr_user.username}!", "primary")
            return redirect(f"/users/{curr_user.username}")
        else:
            flash('User credentials invalid', 'error')
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash('Goodbye!', 'info')
    return redirect('/')

@app.route('/users/<string:username>')
def show_user_details(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.get_or_404(username)
    feedbacks = user.feedbacks
    return render_template('user_details.html', user=user, feedbacks=feedbacks)

@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    if username != session['username']:
        flash("You do not have authorization to delete this account!", "danger")
        return redirect(f'/users/{username}')
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    return redirect('/logout')

@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def user_add_feedback(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    form = FeedbackForm()
    if form.validate_on_submit():
       title = form.title.data
       content = form.content.data
       new_feedback = Feedback(title=title, content=content, username=username)
       db.session.add(new_feedback)
       db.session.commit()
       return redirect(f'/users/{username}') 
    else:
        return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def user_update_feedback(feedback_id):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    user = feedback.user
    if user.username != session['username']:
        flash("You do not have authorization to change this feedback!", "danger")
        return redirect(f'/users/{user.username}')
    if form.validate_on_submit():
       feedback.title = form.title.data
       feedback.content = form.content.data
       db.session.commit()
       return redirect(f'/users/{user.username}') 
    else:
        return render_template('update_feedback.html', form=form)
  
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user
    if user.username != session['username']:
        flash("You do not have authorization to change this feedback!", "danger")
        return redirect(f'/users/{user.username}')
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{user.username}')
