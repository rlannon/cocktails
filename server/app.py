# Cocktails API
# app.py
# Copyright 2020 Riley Lannon

# required imports (flask, etc.)
from flask import  Flask, request, redirect, render_template, url_for, json, jsonify
from flask_cors import CORS, cross_origin
from flaskext.markdown import Markdown
import psycopg2
import os

# custom modules
import db_utilities
import recipe

# initialize the flask app
app = Flask(__name__)
app.json_encoder = recipe.RecipeJSONEncoder

# initialize CORS; for the time being, allow API access on all domains
cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

# initialize the markdown rendering library with the tables extension -- this is used for the API's default homepage
Markdown(app, extensions=['tables', 'markdown.extensions.tables'])

# get the database information from our environment
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_PORT = os.environ.get('DATABASE_PORT')

# connect to the database
db = psycopg2.connect(
    DATABASE_URL,
    port=DATABASE_PORT,
    sslmode='require'
)
cur = db.cursor()

# A const string for the API's base url
API_URL_BASE = "/api/v1/"

# A const string for the API's recipe table
RECIPE_TABLE = "recipes"

#
#   App utilities
#

def query_by_name(name: str) -> list:
    """
    query_by_name
    Searches the database for cocktails with the specified name

    @param  name    The name of the cocktail we are searching for
    @return A list of the recipes that were found
    """
    
    results = db_utilities.fetch(name, cur)
    return results

def query_by_ingredient(ingredients: list) -> list:
    """
    query_by_ingredient
    Searches the database for cocktails that contain any of the listed ingredients

    @param  ingredients The list of ingredients to be used in the search
    @return A list of recipe objects
    """

    # Get a list of names of cocktails containing the specified ingredients
    query = f"""
            SELECT DISTINCT recipe.name
            FROM ((recipe
            INNER JOIN cocktail_ingredient ON cocktail_ingredient.recipe_id = recipe.recipe_id)
            INNER JOIN ingredients ON ingredients.ingredient_id = cocktail_ingredient.ingredient_id)
            WHERE
            """
    for i in range(len(ingredients)):
        query += f"ingredients.name = '{ingredients[i]}'"
        if i < len(ingredients) - 1:
            query += " OR "
    query += ';'

    # Now, execute the query and use fetch() to get all the recipes
    cur.execute(query)
    names = cur.fetchall()

    # iterate through our names, fetch their recipes, and add them to the list -- if nothing was returned (no cocktails contain the ingredients specified), an empty list will be returned (fetchall returns [] if nothing is found)
    recipes = []
    for t in names:
        # use fetch to get recipe objects
        name = t[0] # t is a tuple containing (name,)
        found = db_utilities.fetch(name, cur)

        # concatenate the lists
        recipes += found

    return recipes

def contains_all_ingredients(ingredients: list) -> list:
    """
    contains_all_ingredients
    Searches the database for cocktails containing all of the listed ingredients
    
    @param  ingredients The list of ingredients to be used in the search
    @return A list of recipe object
    """
    return []


#
#   App routes
#

# Get API version and other information
@app.route('/api/v1')
def version():
    return render_template('version.html')

# Get cocktail by name
@app.route(API_URL_BASE + 'cocktail=<name>')
def name(name: str):
    name = name.lower()
    cocktails = query_by_name(name)
    return jsonify(cocktails)

# Get recipes by ingredients
@app.route(API_URL_BASE + 'ingredients=<ingredients>')
def ingredients(ingredients: str):
    # Get the list of ingredients
    ingredients = ingredients.lower()
    ingredients = ingredients.split('+')

    # Send our list to the query
    data = query_by_ingredient(ingredients)
    return jsonify(data)

# Route for index.html
@app.route('/')
def index():
    """
    index
    The route for the API's main index page
    """
    return render_template('index.html')
