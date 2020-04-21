# Cocktails API
# app.py
# Copyright 2020 Riley Lannon

# required imports (flask, etc.)
from flask import  Flask, request, redirect, render_template, url_for, json, jsonify
from flask_cors import CORS, cross_origin
from flaskext.markdown import Markdown
import psycopg2
import os

# initialize the flask app
app = Flask(__name__)

# initialize CORS to allow API access
# todo: uncomment this to enable CORS
# cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

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


# Query data from the database
def get_data(query: str) -> list:
    """
    get_data
    Fetches data from the database

    @param  query   The SQL query to be executed
    
    @return A list of entries returned by the database
    """
    cur = db.cursor()
    cur.execute(query)
    return cur.fetchall()


# Query the database by cocktail name
def query_by_name(name: str) -> list:
    """
    query_by_name
    Queries the database by cocktail name

    @param  name    A string containing the name of the cocktail

    @return A list of entries returned by the database
    """

    # Construct the query; use all lowercase letters for cocktail name
    name = name.lower()
    query = f"SELECT * FROM {RECIPE_TABLE} WHERE name = {name};"
    return get_data(query)


# Get API version and other information
@app.route('/api/v1')
def version():
    return render_template('version.html')


# Route for index.html
@app.route('/')
def index():
    """
    index
    The route for the API's main index page
    """
    return render_template('index.html')
