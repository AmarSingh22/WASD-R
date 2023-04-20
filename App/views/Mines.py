import os
from flask import Flask, Blueprint, render_template,url_for, redirect, request, flash, make_response, jsonify
from .models import Pokemon, UserPokemon, User, db
from flask_login import LoginManager, current_user, login_user, login_required, logout_user


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('Unauthorized!')
    return redirect(url_for('login_page'))

def create_app():
  app = Flask(__name__, static_url_path='/static')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
  app.config['DEBUG'] = True
  app.config['SECRET_KEY'] = 'MySecretKey'
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  db.init_app(app)
  login_manager.init_app(app)
  login_manager.login_view = "login_page"
  app.app_context().push()
  return app

app = create_app()

# Page Routes

#To update
@app.route("/", methods=['GET'])
def login():
  return render_template('login.html')

@app.route("/app", methods=['GET'])
@app.route("/app/<int:pokemon_id>", methods=['GET'])
@login_required
def home_page(pokemon_id=1):
    #pass relevant data to template
    Pokemen =  Pokemon.query.all()
    pokemon = Pokemon.query.get(pokemon_id)
    capture_poke = UserPokemon.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", Pokemen = Pokemen, pokemon = pokemon, capture_poke = capture_poke)

@app.route('/signup', methods=['GET'])
def signup_page():
  return render_template('signup.html')

# Form Action Routes
@app.route('/signup', methods=['POST'])
def signup_action():
  data = request.form 
  newuser = User(username=data['username'], email=data['email'], password=data['password'])
  try:
    db.session.add(newuser)
    db.session.commit() 
    login_user(newuser)
    flash('Account Created!') 
    return redirect(url_for('home_page')) 
  except Exception: 
    db.session.rollback()
    flash("username or email already exists") 
  return redirect(url_for('home_page'))


@app.route('/login', methods=['POST'])
def login_action():
  data = request.form
  user = User.query.filter_by(username=data['username']).first()
  if user and user.check_password(data['password']):
    flash('Logged in successfully.')
    login_user(user)
    return redirect('/app')
  else:
    flash('Invalid username or password')
  return redirect('/')

@app.route('/pokemon/<int:pokemon_id>', methods=['POST'])
@login_required
def capture_pokemon(pokemon_id):
  data = request.form
  current_user.catch_pokemon(pokemon_id, data['pokemon_name'])
  flash('Captured')
  return redirect(url_for('home_page'))


@app.route('/rename-pokemon/<int:user_poke_id>', methods=["POST"])
@login_required
def rename_pokemon_action(user_poke_id):
  data = request.form
  res = current_user.rename_pokemon(user_poke_id, data["new_name"])
  if res:
    flash('Pokemon Renamed!')
  else:
    flash('Pokemon not found or unauthorized')
  return redirect(url_for('home_page'))

@app.route('/release-pokemon/<int:user_poke_id>', methods=["GET"])
@login_required
def release_pokemon_action(user_poke_id):
  res = current_user.release_pokemon(user_poke_id)
  if res == None:
    flash('Invalid id or unauthorized')
  else:
    flash('Pokemon Released')
  return redirect(url_for('home_page'))

@app.route('/logout', methods=['GET'])
@login_required
def logout_action():
  logout_user()
  flash('Logged Out')
  return redirect(url_for('home_page'))



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
