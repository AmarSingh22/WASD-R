from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash
from App.models import *
from App.controllers import create_user, create_Exercise
from flask_login import login_required, login_user, current_user, logout_user
import json
import datetime
import calendar

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('login.html')


@index_views.route('/init', methods=['GET'])
def init():
  db.drop_all()
  db.create_all()
  create_user('bob', 'bobpass')
  with open('Exercises.json') as file:
    data = json.load(file)
    for row in data:
      create_Exercise(row['name'], row['type'], row['muscle'], row['equipment'], row['difficulty'], row['instructions'])
  flash('database Updated')
  return redirect('/')

@index_views.route("/signup", methods=['GET'])
def signup_page():
    return render_template("signup.html")

@index_views.route("/home", methods=['GET'])
@login_required
def home_page():
  user = User.query.get(current_user.id)
  return render_template("home.html", workouts = user.Routines, user_name = user.username, Session_Name = 'YOUR SESSIONS:')

@index_views.route('/workout/<int:workout_id>', methods=["GET"])
@login_required
def workout_page(workout_id):
  workout = UserWorkout.query.get(workout_id)

  if workout and workout.user_id == current_user.id:
    return render_template('workout.html', workout = workout, user_name = current_user.username, Session_Name = workout.name )
  return redirect('/home')

@index_views.route('/exercise', methods=['GET'])
@login_required
def exer_page():
  exercises = Exercise.query.all()
  return render_template("exercise.html", exercises = exercises, user_name = current_user.username, Session_Name = 'Exercises')

@index_views.route('/exercise/<int:exer_id>', methods=['GET'])
@login_required
def exer_info_page(exer_id):
  exercise = Exercise.query.get(exer_id)
  return render_template("exer_info.html", exercise = exercise, user_name = current_user.username, Session_Name = exercise.name )

@index_views.route('/profile', methods=['GET'])
@login_required
def profile_page():
  user = User.query.get(current_user.id)

  if user.weight != None and user.height != None:
    bmi = user.weight/(user.height * user.height)
  else:
    bmi = 0

  if bmi < 18.5:
    status = 'Underweight'
  elif bmi >= 18.5 and bmi < 25:
    status = 'Normal weight'
  elif bmi >= 25 and bmi < 30:
    status = 'Overweight'
  else:
    status = 'Obese'

  bmi = "%.2f" % bmi

  current_time = datetime.datetime.now()
  month = calendar.month_name[current_time.month]

  num_workouts = 0
  for x in current_user.Calendar:
    if x.date.month == current_time.month and x.date.year == current_time.year:
      num_workouts = num_workouts + 1

  return render_template("profile.html", user = user, user_name = current_user.username, Session_Name = current_user.username, bmi = bmi, status = status, month = month, num_workouts = num_workouts )

@index_views.route('/calendar/<int:year>/<int:month>', methods=['GET'])
@index_views.route('/calendar', methods=['GET'])
@login_required
def calendar_page(month = datetime.datetime.now().month, year = datetime.datetime.now().year):
  month_name = calendar.month_name[month]

  if month == 0:
    month = 12
    year = year - 1
  if month == 13:
    month = 1
    year = year + 1

  num_workouts = 0
  for x in current_user.Calendar:
    if x.date.month == month and x.date.year == year:
      num_workouts = num_workouts + 1

  return render_template("calendar.html", user = current_user, user_name = current_user.username, Session_Name = month_name, num_workouts = num_workouts, month = month, year = year )

@index_views.route('/contact-us', methods=['GET'])
@login_required
def contact_page():
  return render_template("contact.html", user_name = current_user.username, Session_Name = 'Contact Us' )