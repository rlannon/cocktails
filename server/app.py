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

def query_by_ingredient(ingredients: list) -> list:
    """
    query_by_ingredient
    Searches the database for cocktails that contain any of the listed ingredients

    @param  ingredients The list of ingredients to be used in the search
    @return A list of recipe objects
    """
    return []

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

@app.route(API_URL_BASE + 'ingredients=<ingredients>')
def ingredients(ingredients: str):
    print("ingredients: " + ingredients)
    ingredients = ingredients.lower()
    data = query_by_ingredient(ingredients)
    print(data)
    return render_template('version.html')

# Route for index.html
@app.route('/')
def index():
    """
    index
    The route for the API's main index page
    """
    return render_template('index.html')
