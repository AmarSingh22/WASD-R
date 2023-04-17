from App.database import db
from .user import *

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

class Workout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  Exercises = db.relationship('WorkoutExercises', backref='workout', lazy=True, cascade="all, delete-orphan")

  def __init__(self, name):
    self.name = name

  def get_json(self):
    return{
      "id":self.id,
      "name":self.name,
    }

  def __repr__(self):
    return f'<Workout: {self.id} - {self.name}>'
  pass

class UserWorkout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

  def get_json(self):
    return{
      "id":self.id,
      "Workout_id": self.workout_id
    }

  def __repr__(self):
    return f'<Workout: {self.id} | {self.user_id} | {self.workout_id}>'
  pass


class WorkoutExercises(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
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