from App.database import db
from .user import *

import datetime

class Exercise(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True ,nullable=False)
  ex_type = db.Column(db.String(80), nullable=False)
  muscle= db.Column(db.String(80), nullable=False)
  equipment = db.Column(db.String(80), nullable=False)
  difficulty = db.Column(db.String(80), nullable=False)
  instructions = db.Column(db.String(18000))

  def __init__(self, name, ex_type, muscle, equipment, difficulty, instructions):
    self.name= name
    self.ex_type= ex_type
    self.muscle= muscle
    self.equipment= equipment
    self.difficulty= difficulty
    self.instructions= instructions

  def __repr__(self):
    return f'<Exercise {self.ex_id} {self.name} - {self.muscle}>'
  pass

class UserWorkout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(80), nullable=False)
  Exercises = db.relationship('WorkoutExercises', backref='userworkout', lazy=True, cascade="all, delete-orphan")

  def __init__(self, name):
    self.name = name
    
  def add_exercise(self, exercise_id):
    new_exercise = WorkoutExercises(exercise_id = exercise_id)
    new_exercise.workout_id = self.id
    self.Exercises.append(new_exercise)
    db.session.add(self)
    db.session.commit()
    return new_exercise

  def update_sets(self, exercise_id, sets):
    exercise = WorkoutExercises.query.get(exercise_id)
    if exercise:      
      exercise.sets = sets
      db.session.add(exercise)
      db.session.commit()
      return True
    return None

  def update_reps(self, exercise_id, reps):
    exercise = WorkoutExercises.query.get(exercise_id)
    if exercise:
      exercise.reps = reps
      db.session.add(exercise)
      db.session.commit()
      return True
    return None

  def del_exercise(self, exercise_id):
    exercise = WorkoutExercises.query.get(exercise_id)
    if exercise:
      db.session.delete(exercise)
      db.session.commit()
      return True
    return None
  
  def get_json(self):
    return{
      "id":self.id,
      "user_id": self.user_id,
      "name": self.name
    }

  def __repr__(self):
    return f'<Workout: {self.id} - {self.name} {self.user_id} | >'
  pass

class WorkoutExercises(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey('user_workout.id'), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
  sets = db.Column(db.Integer, nullable=False, default=1)
  reps = db.Column(db.Integer, nullable=False, default=1)

  def __init__(self, sets, reps):
    self.sets = sets
    self.reps = reps

  def get_json(self):
    return{
      "id":self.id,
      "workout_id":self.workout_id,
      "exercise_id":self.exercise_id,
      "sets":self.sets,
      "reps":self.reps
    }

  def __repr__(self):
    return f'<Workout: {self.workout_id} - {self.exercise_id} sets: {self.sets} reps: {self.reps}>'
  pass

class WorkoutCalender(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(80), nullable=False)
  date = db.Column(db.Date, default=datetime.datetime.now())

  def __init__(self, name, date):
    self.name = name
    self.date = date

  def get_json(self):
    return{
      "id":self.id,
      "user_id": self.user_id,
      "name": self.name,
      "date" : self.date
    }

  def __repr__(self):
    return f'<Workout: {self.id} - {self.name} {self.user_id} at {self.date} >'
