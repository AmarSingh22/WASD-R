from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class UserPokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  Pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
  name = db.Column(db.String(80), nullable=False)

  def __init__(self, name):
    self.name = name

  def get_json(self):
    pkmn = Pokemon.query.filter_by(id = self.Pokemon_id).first()
    return{
      "id":self.id,
      "name":self.name,
      "species":pkmn.name
    }

  def __repr__(self):
    return f'<UserPokemon: {self.id} | {self.User.username} | {self.Pokemon_id} |{self.name}>'
  pass

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  Userpokemons = db.relationship('UserPokemon', backref='user', lazy=True, cascade="all, delete-orphan")


  def __init__(self, username, email, password):
    self.username= username
    self.email= email
    self.set_password(password)

  def catch_pokemon(self, pokemon_id, name):
    new_pokemon = UserPokemon(name = name)
    new_pokemon.Pokemon_id = pokemon_id
    new_pokemon.user_id = self.id
    self.Userpokemons.append(new_pokemon)
    db.session.add(self)
    db.session.commit()
    return new_pokemon

  def release_pokemon(self, pokemon_id, name):
    pokemon = UserPokemon.query.filter_by(id=pokemon_id, name = name, user_id=self.id).first()
    if pokemon:
      db.session.delete(pokemon)
      db.session.commit()
      return True
    return None

  def rename_pokemon(self, pokemon_id, name):
    pokemon = UserPokemon.query.filter_by(id = pokemon_id, user_id = self.id).first()
    if pokemon:
      pokemon.name = name
      db.session.add(pokemon)
      db.session.commit()
      return True
    return None

  def set_password(self, password):
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return f'<User {self.id} {self.username} - {self.email}>'
  pass

class Pokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), unique=True, nullable=False)
  attack = db.Column(db.Integer, nullable=False)
  defense = db.Column(db.Integer, nullable=False)
  hp = db.Column(db.Integer, nullable=False)
  height = db.Column(db.Integer)
  weight = db.Column(db.Integer)
  sp_attack = db.Column(db.Integer, nullable=False)
  sp_defense = db.Column(db.Integer, nullable=False)
  speed = db.Column(db.Integer, nullable=False)
  type1 = db.Column(db.String(40), nullable=False)
  type2 = db.Column(db.String(40))
    
  def __init__(self, name, attack, defense, hp, height, weight, sp_attack, sp_defense, speed, type1, type2):
    self.name = name
    self.attack = attack
    self.defense = defense
    self.hp = hp
    self.height = height
    self.weight = weight
    self.sp_attack = sp_attack
    self.sp_defense = sp_defense
    self.speed = speed 
    self.type1 = type1
    self.type2 = type2

  def get_json(self):
    
    return {
      "pokemon_id": self.id,
      "name":self.name,
      "attack":self.attack, 
      "defense":self.defense,
      "sp_attack":self.sp_attack,
      "sp_defense":self.sp_defense,
      "speed":self.speed,
      "hp":self.hp,
      "height":self.height,
      "weight":self.weight, 
      "type2":self.type2,
      "type1":self.type1
    }

  def __repr__(self):
    return f'<{self.id} {self.name} {self.type1} {self.type2}: {self.hp} {self.attack} {self.defense} {self.sp_attack} {self.sp_defense} {self.speed} {self.height} {self.weight}>'      
  pass
