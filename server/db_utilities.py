# Cocktails API
# db_utilities.py
# Copyright 2020 Riley Lannon

# Some utility functions for inserting recipes into and obtaining recipes from the database

import recipe

#
#   Normalization functions
#

def normalize_strings(ingredients: list, cur) -> list:
    """
    normalize_strings
    Normalizes the string names supplied to what the database expects

    The database expects fairly particular ingredient/garnish/drinkware names, but users might supply slightly different input parameters -- we want to be able to normalize for that, so this function takes common variations and swaps them for what our database expects
    This function utilizes the database table 'normalize' to make the swaps

    @param  ingredients The list of ingredients to normalize
    @param  cur The database cursor
    @return A list of normalized names
    @throws This function will only throw exceptions in the event of a malformed SQL query or some other similar error
    """

    # Iterate over the ingredients and normalize as we go
    normalized = []
    for i in ingredients:
        # first, make sure it's lowercase
        n = i.lower()

        # see if we have a normalized version; if not, push the original (might be valid, might not)
        cur.execute(f"SELECT db_name FROM normalize WHERE supplied_name = '{n}';")
        r = cur.fetchone()
        if r is None:
            normalized.append(n)
        else:
            normalized.append(r[0])
    
    return normalized

#
#   Fetch / retrieval
#

def insert(r: recipe.recipe, cur) -> None:
    """
    insert
    Inserts a recipe, contained within the object 'r', into the database

    @param  r   An object containing the recipe we wish to insert
    @param  cur The database cursor
    @return None
    @throws This function throws an exception if it encounters an error
    """

    return

def fetch(name: str, cur) -> list:
    """
    fetch
    Fetches a recipe for the cocktail with the given name from the database

    @param  name    The name of the cocktail we are fetching
    @param  cur The database cursor
    @return A list of recipe objects containing the matching cocktail recipes
    @throws This function throws an exception if it encounters an error
    """

    # get the basic cocktail information from 'recipe'
    query = f"""
    SELECT recipe.recipe_id, recipe.name, recipe.instructions, recipe.notes
    FROM recipe
    WHERE recipe.name = '{name}';
    """
    cur.execute(query)
    recipe_data = cur.fetchall()

    # we may have found multiple recipes, so iterate through the ones that were found
    recipes = []
    for r in recipe_data:
        # Give the indices their own labels for ease of use
        recipe_id = r[0]
        recipe_name = r[1]
        recipe_instructions = r[2]
        recipe_notes = r[3]

        # Get the drinkware
        query = f"""
        SELECT drinkware.name
        FROM ((cocktail_drinkware
        INNER JOIN drinkware ON drinkware.drinkware_id = cocktail_drinkware.drinkware_id)
        INNER JOIN recipe ON recipe.recipe_id = cocktail_drinkware.recipe_id)
        WHERE recipe.recipe_id = {recipe_id};
        """
        cur.execute(query)
        drinkware_data = cur.fetchall()

        # now, iterate through the tuples in drinkware_data and 
        drinkware = []
        if drinkware_data is not None:
            # 'drinkware_data' contains tuples of (name,)
            for i in drinkware_data:
                drinkware.append(i[0])
        else:
            raise Exception("Drinkware not found")

        # Get the serving info
        query = f"""
        SELECT served.name
        FROM ((cocktail_served
        INNER JOIN served ON served.served_id = cocktail_served.served_id)
        INNER JOIN recipe ON cocktail_served.recipe_id = recipe.recipe_id)
        WHERE recipe.recipe_id = {recipe_id};
        """
        cur.execute(query)
        served_data = cur.fetchall()

        # do the same thing we did for the drinkware
        served = []
        if served_data is not None:
            for i in served_data:
                served.append(i[0])
        else:
            raise Exception("Serving info not found")

        # Get the garnish info
        query = f"""
        SELECT garnish.name
        FROM ((cocktail_garnish
        INNER JOIN garnish ON cocktail_garnish.garnish_id = garnish.garnish_id)
        INNER JOIN recipe ON cocktail_garnish.recipe_id = recipe.recipe_id)
        WHERE recipe.recipe_id = {recipe_id};
        """
        cur.execute(query)
        garnish_data = cur.fetchall()

        garnishes = []
        if garnish_data is not None:
            for i in garnish_data:
                garnishes.append(i[0])
        else:
            raise Exception("Garnish info not found")

        # Now, get all of the ingredients in the recipe
        query = f"""
        SELECT ingredients.name, cocktail_ingredient.measure_number, cocktail_ingredient.unit_of_measurement
        FROM cocktail_ingredient
        INNER JOIN ingredients ON ingredients.ingredient_id = cocktail_ingredient.ingredient_id
        WHERE cocktail_ingredient.recipe_id = {recipe_id};
        """
        cur.execute(query)
        ingredients = cur.fetchall()

        # since the ingredients query returns exactly what we want (tuples of (name,measure,unit)), we don't need to modify them -- just check to make sure we got results
        if ingredients is None or len(ingredients) == 0:
            raise Exception("Ingredients not found")

        to_add = recipe.recipe(recipe_name, ingredients, garnishes, drinkware, served, recipe_instructions, recipe_notes)
        recipes.append(to_add)

    # return our list of recipes
    return recipes
