from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.database import Pokemon, db

pokemon = Blueprint('pokemon', __name__, template_folder = 'templates')
BASE_URL = '/pokemon'

@pokemon.route(BASE_URL, methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pokemon_name = request.form['name']
        primary = request.form['primary']
        secondary = request.form['secondary']
        new_pokemon = Pokemon(name=pokemon_name, primary_type = primary,
            secondary_type = secondary)
        try:
            db.session.add(new_pokemon)
            db.session.commit()
            return redirect(BASE_URL)
        except:
            return redirect(BASE_URL)
    else:
        pokemonList = Pokemon.query.order_by(Pokemon.name).all()
        return render_template('pokemon.html', pokemonList=pokemonList, url='/pokemon')

@pokemon.route(BASE_URL + '/add/', methods = ['POST'])
def addPokemon():
    return "Add Pokemon here"

@pokemon.route(BASE_URL + '/update/<int:id>', methods=['GET', 'POST'])
def updatePokemon(id):
    pokemon = Pokemon.query.get_or_404(id)
    if request.method == 'POST':
        pokemon.name = request.form['name']
        pokemon.primary_type = request.form['primary']
        pokemon.secondary_type = request.form['secondary']
        try:
            db.session.commit()
            return redirect('/pokemon')
        except:
            return "There was an issue updating a pokemon"
    else:
        return render_template('pokemon/update.html', pokemon=pokemon)

@pokemon.route(BASE_URL + '/delete/<int:id>')
def delete(id):
    pokemon_to_delete = Pokemon.query.get_or_404(id)

    try:
        db.session.delete(pokemon_to_delete)
        db.session.commit()
        return redirect(BASE_URL)
    except:
        return "Error in deleting Pokemon"

@pokemon.route('/add')
def add():
    return "Add..."

@pokemon.route('/pokemon/foobar')
def nested():
    return "Hello World Pokemon foobar"