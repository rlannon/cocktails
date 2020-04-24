# Cocktails API
# db_utilities.py
# Copyright 2020 Riley Lannon

# Some utility functions for inserting recipes into and obtaining recipes from the database

import recipe

def insert(r: recipe.recipe) -> None:
    """
    insert
    Inserts a recipe, contained within the object 'r', into the database

    @param  r   An object containing the recipe we wish to insert
    @return None
    @throws This function throws an exception if it encounters an error
    """

    return

def fetch(name: str) -> recipe.recipe:
    """
    fetch
    Fetches a recipe for the cocktail with the given name from the database

    @param  name    The name of the cocktail we are fetching
    @return A recipe object containing the fetched cocktail recipe
    @throws This function throws an exception if it encounters an error
    """

    return
