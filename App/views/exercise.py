from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from App.models import User, Exercise, UserWorkout, WorkoutExercises, WorkoutCalender


exer_views = Blueprint('exer_views', __name__, template_folder='../templates')


#Page Actions .................................................................................

#User Update Actions
@exer_views.route('/profile/gender', methods=['POST'])
@login_required
def update_gender_action():
  data = request.form
  current_user.update_gender(data['gender'])
  return redirect('/profile')

@exer_views.route('/profile/height', methods=['POST'])
@login_required
def update_height_action():
  data = request.form
  current_user.update_height(data['height'])
  return redirect('/profile')

@exer_views.route('/profile/weight', methods=['POST'])
@login_required
def update_weight_action():
  data = request.form
  current_user.update_weight(data['weight'])
  return redirect('/profile')

#Workout Actions
@exer_views.route('/create-workout', methods=['POST'])
@login_required
def add_workout_action():
  data = request.form
  current_user.add_workout(data['name'])
  flash('Added')
  return redirect('/home')

@exer_views.route('/rename-workout/<int:workout_id>', methods=["POST"])
@login_required
def update_workout_action(workout_id):
  data = request.form
  workout = UserWorkout.query.get(workout_id)

  if workout and workout.user_id == current_user.id :
    current_user.update_workout(workout_id, data["new_name"])
    flash('Workout renamed')
  else:
    flash('Workout not found or unauthorized')
  return redirect('/home')

@exer_views.route('/delete-workout/<int:workout_id>', methods=["GET"])
@login_required
def del_workout_action(workout_id):
  workout = UserWorkout.query.get(workout_id)
  if workout and workout.user_id == current_user.id :
    current_user.del_workout(workout_id)
    flash('Workout Deleted')
  else:
    flash('Invalid id or unauthorized')
  return redirect('/home')


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
    return redirect(f'/workout/{workout.id}')

@exer_views.route('/workout/<int:workout_id>/exercise-reps/<int:work_exer_id>', methods=["POST"])
@login_required
def update_reps_action(workout_id, work_exer_id):
  data = request.form
  workout = UserWorkout.query.get(workout_id)
  workoutExer = WorkoutExercises.query.get(work_exer_id)

  if workoutExer and workout.user_id == current_user.id:
    workout.update_reps(work_exer_id, data['reps'])
  return redirect(f'/workout/{workout_id}')

@exer_views.route('/workout/<int:workout_id>/exercise-sets/<int:work_exer_id>', methods=["POST"])
@login_required
def update_sets_action(workout_id, work_exer_id):
  data = request.form
  workout = UserWorkout.query.get(workout_id)
  workoutExer = WorkoutExercises.query.get(work_exer_id)

  if workoutExer and workout.user_id == current_user.id:
    workout.update_sets(work_exer_id, data['sets'])
  return redirect(f'/workout/{workout_id}')

@exer_views.route('/workout/<int:workout_id>/delete-exercise/<int:work_exer_id>', methods=["GET"])
@login_required
def delete_exercise_action(workout_id, work_exer_id):
  workout = UserWorkout.query.get(workout_id)
  workoutExer = WorkoutExercises.query.get(work_exer_id)

  if workoutExer == None or workout.user_id != current_user.id:
    flash('Invalid id or unauthorized')
  else:
    flash('Exercise deleted')
    workout.del_exercise(work_exer_id)
  return redirect(f'/workout/{workout_id}')

@exer_views.route('/workout/<int:workout_id>/workout-completed', methods=["GET"])
@login_required
def workout_completed_action(workout_id):
  workout = UserWorkout.query.get(workout_id)

  if workout and workout.user_id == current_user.id:
    current_user.workout_Completed(workout.name)
  return redirect('/home')
