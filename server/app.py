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

    # Do some preliminary checks to avoid errors
    if ingredients is None or len(ingredients) == 0:
        # Return an empty list if we didn't get any ingredients
        return []
    elif len(ingredients) == 1:
        # Otherwise, if we only have one ingredient, just send this to query_by_ingredient
        return query_by_ingredient(ingredients)

    # First, we need the ingredient ids
    ids = []
    for i in ingredients:
        query = f"""
        SELECT ingredient_id
        FROM ingredients
        WHERE name = '{i}';
        """
        cur.execute(query)
        i_id = cur.fetchone()

        # if we couldn't find the ingredient, raise an exception
        if i_id is None:
            raise Exception("No such ingredient")   # handle this by removing ingredient?

        # otherwise, we have a tuple containing (ingredient_id,)
        ids.append(i_id[0])

    # Now, construct the query with a self join on cocktail_ingredient
    query = f"""
    SELECT {ingredients[0]}.recipe_id
    FROM 
    """
    for i in range(len(ingredients)):
        query += f"cocktail_ingredient {ingredients[i]}"
        if i < len(ingredients) - 1:
            query += ", "
        else:
            query += " "
    
    # make sure all ingredient ids are equal
    query += "WHERE "
    for i in range(len(ingredients)):
        query += f"{ingredients[i]}.ingredient_id = {ids[i]} AND "
    
    # make sure the recipe ids are equal among all of the table names
    for i in range(1, len(ingredients)):
        query += f"{ingredients[i]}.recipe_id = {ingredients[0]}.recipe_id"
        if i < len(ingredients) - 1:
            query += " AND "
        else:
            query += ";"

    # Now, execute the query
    cur.execute(query)
    results = cur.fetchall()

    # Iterate through the results and get the recipe names
    names = []
    for r in results:
        # Fetch the name corresponding with the obtained recipe id
        cur.execute(f"SELECT name FROM recipe WHERE recipe_id = {r[0]};")
        r_name = cur.fetchone()
        
        # Make sure we got a result; append it to our names list
        if r_name is None:
            raise Exception("No such recipe in table with the given id")
        names.append(r_name[0])
    
    # Now, get the recipes
    recipes = []
    for name in names:
        recipes += db_utilities.fetch(name, cur)

    return recipes

# Query by cocktail drinkware
def query_by_drinkware(drinkware: str) -> list:
    """
    query_by_drinkware
    Returns a list of recipes that are served in the supplied drinkware
    """

    query = f"SELECT drinkware_id FROM drinkware WHERE name = '{drinkware}';"
    cur.execute(query)

    drinkware_id = cur.fetchone()
    if drinkware_id is None:
        raise Exception("No drinkware found")
    
    drinkware_id = drinkware_id[0]  # returns tuple (drinkware_id,)
    
    # now, query for all cocktails using that drinkware
    query = f"""
    SELECT recipe_id
    FROM cocktail_drinkware
    WHERE drinkware_id = {drinkware_id};
    """
    cur.execute(query)
    recipe_ids = cur.fetchall()

    # now, fetch all recipe data based on the recipe id
    recipes = []
    for r_id in recipe_ids:
        recipes.append(
            db_utilities.fetch_by_id(
                r_id[0],
                cur
            )
        )

    return recipes

def query_by_served(served: str) -> list:
    """
    query_by_served
    Finds recipes based on how they are served

    @param  served  How the cocktail is served (e.g., on the rocks, straight up)
    """
    cur.execute(f"SELECT served_id FROM served WHERE name = '{served}';")
    result = cur.fetchone()
    if result is None:
        raise Exception("Cannot find serving method")
    served_id = result[0]
    cur.execute(f"SELECT recipe_id FROM cocktail_served WHERE served_id = {served_id};")
    recipe_ids = cur.fetchall()
    recipes = []
    for r_id in recipe_ids:
        recipes.append(db_utilities.fetch_by_id(r_id[0], cur))
    return recipes


#
#   App routes
#

# Get API version and other information
@app.route('/api/v1')
def version():
    return render_template('version.html')

# Get cocktail by name
@app.route(API_URL_BASE + 'name/<name>')
@app.route(API_URL_BASE + 'cocktail/<name>')
def name(name: str):
    name = name.lower()
    cocktails = query_by_name(name)
    return jsonify(cocktails)

# Get all ingredients
@app.route(API_URL_BASE + 'ingredients')
def list_ingredients():
    cur.execute(
        f"""
        SELECT DISTINCT name
        FROM ingredients
        ORDER BY name;
        """
    )
    results = cur.fetchall()

    ingredients = []
    for i in results:
        ingredients.append(i[0])

    return jsonify(ingredients)

# Get recipes by ingredients
@app.route(API_URL_BASE + 'ingredients/<ingredients>')
def ingredients(ingredients: str):
    # Get the list of ingredients
    ingredients = ingredients.split('+')
    ingredients = db_utilities.normalize_strings(ingredients, cur)

    # Send our list to the query
    data = query_by_ingredient(ingredients)
    return jsonify(data)

# Get recipes containing all of the specified ingredients
@app.route(API_URL_BASE + 'contains/<ingredients>')
def contains(ingredients: str):
    # Get the list of ingredients
    ingredients = ingredients.split('+')
    ingredients = db_utilities.normalize_strings(ingredients, cur)

    # Send our list to the query
    data = contains_all_ingredients(ingredients)
    return jsonify(data)

# todo: option for cocktails containing *only* the specified ingredients (but not necessarily *all* of them)

@app.route(API_URL_BASE + 'garnish')
def all_garnishes():
    cur.execute(
        """
        SELECT name
        FROM garnish
        ORDER BY name;
        """
    )
    data = cur.fetchall()
    garnishes = []
    for i in data:
        garnishes.append(i[0])
    return jsonify(garnishes)

# todo: get recipes by garnish

# Get all drinkware
@app.route(API_URL_BASE + 'drinkware')
def all_drinkware():
    cur.execute(
        f"""
        SELECT name
        FROM drinkware
        ORDER BY name;
        """
    )
    data = cur.fetchall()
    drinkware = []
    for i in data:
        drinkware.append(i[0])
    return jsonify(drinkware)

# Get recipes by drinkware
@app.route(API_URL_BASE + 'drinkware/<drinkware>')
def drinkware(drinkware: str):
    # Normalize the drinkware
    drinkware = db_utilities.normalize_string(drinkware, cur)

    # Send it to our query
    data = query_by_drinkware(drinkware)
    return jsonify(data)

# Get all serving methods
@app.route(API_URL_BASE + 'served')
def all_served():
    cur.execute(
        """
        SELECT name
        FROM served
        ORDER BY name;
        """
    )
    data = cur.fetchall()
    served = []
    for i in data:
        served.append(i[0])
    return jsonify(served)

# Get recipes by how they are served
@app.route(API_URL_BASE + 'served/<served>')
def served(served: str):
    # Normalize the string
    served = db_utilities.normalize_string(served, cur)

    # Send it to our querying function
    data = query_by_served(served)
    return jsonify(data)

# Custom searches
# @app.route(API_URL_BASE + 'custom')
#   todo: custom searches

# Route for index.html
@app.route('/')
def index():
    """
    index
    The route for the API's main index page
    """
    return render_template('index.html')
