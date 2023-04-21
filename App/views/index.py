from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import *
from App.controllers import create_user
from flask_login import login_required, login_user, current_user, logout_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('login.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route("/signup", methods=['GET'])
def signup_page():
    return render_template("signup.html")

@index_views.route("/home", methods=['GET'])
@login_required
def home_page():
  user = User.query.get(current_user.id)
  return render_template("home.html", workouts = user.Routines, user_name = user.username)

@index_views.route('/workout/<int:workout_id>', methods=["GET"])
@login_required
def workout_page(workout_id):
  workout = UserWorkout.query.get(workout_id)

  if workout and workout.user_id == current_user.id:
    return render_template('workout.html', workout = workout)
  return redirect(url_for('home_page'))

@index_views.route('/exercise', methods=['GET'])
@login_required
def exer_page():
  exercises = Exercise.query.all()
  return render_template("exercise.html", exercises = exercises)

@index_views.route('/exercise/<int:exer_id>', methods=['GET'])
@login_required
def exer_info_page(exer_id):
  exercise = Exercise.query.get(exer_id)
  return render_template("exer_info.html", exercise = exercise)

@index_views.route('/profile', methods=['GET'])
@login_required
def profile_page():
  user = User.query.get(current_user.id)
  return render_template("profile.html", user = user)

@index_views.route('/calendar', methods=['GET'])
@login_required
def calendar_page():
  user = User.query.get(current_user.id)
  return render_template("calendar.html", user = user)

@index_views.route('/contact-us', methods=['GET'])
@login_required
def contact_page():
  return render_template("contact.html")