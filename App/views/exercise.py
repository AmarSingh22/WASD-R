from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from App.models import *


exer_views = Blueprint('exer_views', __name__, template_folder='../templates')

#Views Url
@exer_views.route("/", methods=['GET'])
def login_page():
    return render_template("login.html")

@exer_views.route("/signup", methods=['GET'])
def signup_page():
    return render_template("signup.html")

@exer_views.route("/home", methods=['GET'])
@login_required
def home_page():
  workouts = UserWorkout.query.filter_by(user_id == jwt_current_user.id).all()
  return render_template("home.html", workouts = workouts)

@exer_views.route('/workout/<int:workout_id>', methods=["GET"])
@login_required
def workout_page(workout_id):
  workout = UserWorkout.query.get(workout_id)

  if workout and workout.user_id == jwt_current_user.id:
    return render_template('workout.html', workout = workout)
  return redirect(url_for('home_page'))

@exer_views.route('/exercise', methods=['GET'])
@login_required
def exer_page():
  exercises = Exercise.query.all()
  render_template("exercise.html", exercises = exercises)

@exer_views.route('/exercise/<int:exer_id>', methods=['GET'])
@login_required
def exer_info_page(exer_id):
  exercise = Exercise.query.get(exer_id)
  render_template("exer_info.html", exercise = exercise)

@exer_views.route('/profile', methods=['GET'])
@login_required
def profile_page():
  user = User.query.get(jwt_current_user.id)
  render_template("profile.html", user = user)

@exer_views.route('/calendar', methods=['GET'])
@login_required
def calendar_page():
  user = User.query.get(jwt_current_user.id)
  render_template("calendar.html", user = user)

#Page Actions .................................................................................

#User Update Actions
@exer_views.route('/profile/gender>', methods=['POST'])
@login_required
def update_gender_action():
  data = request.form
  jwt_current_user.update_gender(data['gender'])
  return redirect(url_for('profile_page'))

@exer_views.route('/profile/height>', methods=['POST'])
@login_required
def update_height_action():
  data = request.form
  jwt_current_user.update_height(data['height'])
  return redirect(url_for('profile_page'))

@exer_views.route('/profile/weight>', methods=['POST'])
@login_required
def update_weight_action():
  data = request.form
  jwt_current_user.update_weight(data['weight'])
  return redirect(url_for('profile_page'))

#Workout Actions
@exer_views.route('/create-workout', methods=['POST'])
@login_required
def add_workout_action():
  data = request.form
  jwt_current_user.add_workout(data['name'])
  flash('Added')
  return redirect(url_for('home_page'))

@exer_views.route('/rename-workout/<int:workout_id>', methods=["POST"])
@login_required
def update_workout_action(workout_id):
  data = request.form
  res = jwt_current_user.update_workout(workout_id, data["new_name"])
  if res:
    flash('Workout renamed')
  else:
    flash('Workout not found or unauthorized')
  return redirect(url_for('home_page'))

@exer_views.route('/delete-workout/<int:workout_id>', methods=["GET"])
@login_required
def del_workoutn_action(workout_id):
  res = jwt_current_user.del_workout(workout_id)
  if res == None:
    flash('Invalid id or unauthorized')
  else:
    flash('Workout Deleted')
  return redirect(url_for('home_page'))


#Workout Exercises Actions
@exer_views.route('/exercise/<int:exer_id>', methods=['POST'])
@login_required
def add_exercise_action(exer_id):
    data = request.form
    workout = UserWorkout.query.filter_by(name = data['workout_name']).first()
    if workout and workout.user_id == current_user.id:
        workout.add_exercise(exer_id)
        flash('Exercise added')
    else:
        flash('Workout name does not exist')
    return redirect(url_for('exer_page'))

@exer_views.route('/workout/<int:workout_id>/exercise-reps/<int:work_exer_id>', methods=["POST"])
@login_required
def update_reps_action(workout_id, work_exer_id):
  data = request.form
  workout = UserWorkout.query.get(workout_id)
  workoutExer = WorkoutExercises.query.get(work_exer_id)

  if workoutExer and workout.user_id == jwt_current_user.id:
    workout.update_reps(work_exer_id, data['reps'])
  return redirect(url_for('workout_page'))

@exer_views.route('/workout/<int:workout_id>/exercise-sets/<int:work_exer_id>', methods=["POST"])
@login_required
def update_sets_action(workout_id, work_exer_id):
  data = request.form
  workout = UserWorkout.query.get(workout_id)
  workoutExer = WorkoutExercises.query.get(work_exer_id)

  if workoutExer and workout.user_id == jwt_current_user.id:
    workout.update_sets(work_exer_id, data['sets'])
  return redirect(url_for('workout_page'))

@exer_views.route('/workout/<int:workout_id>/delete-exercise/<int:work_exer_id>', methods=["GET"])
@login_required
def delete_exercise_action(workout_id, work_exer_id):
  workout = UserWorkout.query.get(workout_id)
  workoutExer = WorkoutExercises.query.get(work_exer_id)

  if workoutExer == None or workout.user_id == jwt_current_user.id:
    flash('Invalid id or unauthorized')
  else:
    flash('Exercise deleted')
    workout.del_exercise()
  return redirect(url_for('workout_page'))

@exer_views.route('/workout/<int:workout_id>/workout-completed', methods=["POST"])
@login_required
def workout_completed_action(workout_id):
  workout = UserWorkout.query.get(workout_id)

  if workout and workout.user_id == jwt_current_user.id:
    jwt_current_user.workout_Completed(workout.name)
  return redirect(url_for('calendar_page'))