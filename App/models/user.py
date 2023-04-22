from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from .exercise import *

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(1))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    Routines = db.relationship('UserWorkout', backref='user', lazy=True, cascade="all, delete-orphan")
    Calendar = db.relationship('WorkoutCalender', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }
    def add_workout(self, name):
        new_workout = UserWorkout(name = name)
        new_workout.user_id = self.id
        self.Routines.append(new_workout)
        db.session.add(self)
        db.session.commit()
        return new_workout

    def del_workout(self, workout_id):
        workout = UserWorkout.query.get(workout_id)
        if workout:
            db.session.delete(workout)
            db.session.commit()
            return True
        return None

    def update_workout(self, workout_id, name):
        workout = UserWorkout.query.get(workout_id)
        if workout:
            workout.name = name
            db.session.add(workout)
            db.session.commit()
            return True
        return None

    def update_gender(self, gender):
        self.gender = gender
        db.session.add(self)
        db.session.commit()
        return True
    def update_height(self, height):
        self.height = height
        db.session.add(self)
        db.session.commit()
        return True
    def update_weight(self, weight):
        self.weight = weight
        db.session.add(self)
        db.session.commit()
        return True

    def workout_Completed(self, name):
        workout_com = WorkoutCalender(name = name)
        workout_com.user_id = self.id
        self.Calendar.append(workout_com)
        db.session.add(self)
        db.session.commit()
        return workout_com

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

