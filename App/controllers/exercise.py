from App.models import User, Exercise
from App.database import db


def create_Exercise(name, ex_type, muscle, equipment, difficulty, instructions):
    new_exercise = Exercise(name = name, ex_type = ex_type , muscle = muscle, equipment = equipment, difficulty = difficulty, instructions= instructions)
    db.session.add(new_exercise)
    db.session.commit()
    return new_exercise