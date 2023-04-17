from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user


exer_views = Blueprint('exer_views', __name__, template_folder='../templates')

@exer_views.route("/home", methods=['GET'])
@login_required
def home_page():
    return render_template("home.html")

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





@exer_views.route('/exercise/<int:exer_id>', methods=['POST'])
@login_required
def add_exercise_action(exer_id):
    data = request.form
    workout = UserWorkout.query.filter_by(name = data['workout_name'])
    if workout and workout.user_id == current_user.id:
        workout.add_exercise(exer_id)
        flash('Exercise added')
    else:
        flash('Workout name does not exist')
    return redirect(url_for('home_page'))



@exer_views.route('/exercise-reps/<int:work_exer_id>', methods=["POST"])
@login_required
def update_reps_action(work_exer_id):
  data = request.form
  workoutExer = WorkoutExercises.query.get(work_exer_id)
  workout = UserWorkout.query.get(workoutExer.workout_id)

  if workoutExer and workout.user_id == current_user.id:
    workoutExer.update_reps(data['reps'])
  return redirect(url_for('home_page'))

@exer_views.route('/exercise-sets/<int:work_exer_id>', methods=["POST"])
@login_required
def update_sets_action(work_exer_id):
  data = request.form
  workoutExer = WorkoutExercises.query.get(work_exer_id)
  workout = UserWorkout.query.get(workoutExer.workout_id)

  if workoutExer and workout.user_id == current_user.id:
    workoutExer.update_sets(data['sets'])
  return redirect(url_for('home_page'))



@exer_views.route('/delete-exercise/<int:work_exer_id>', methods=["GET"])
@login_required
def release_pokemon_action(work_exer_id):
  workoutExer = WorkoutExercises.query.get(work_exer_id)
  workout = UserWorkout.query.get(workoutExer.workout_id)

  if workoutExer == None or workout.user_id == current_user.id:
    flash('Invalid id or unauthorized')
  else:
    flash('Pokemon Released')
  return redirect(url_for('home_page'))