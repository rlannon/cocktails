# Cocktails API
# recipe.py
# Copyright 2020 Riley Lannon

# Contains classes to hold cocktail recipes and ingredients

from flask.json import JSONEncoder

class RecipeJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, recipe):
            return obj.__dict__
        elif isinstance(obj, cocktail_ingredient):
            return obj.__dict__
        else:
            return super(RecipeJSONEncoder, self).default(obj)


class cocktail_ingredient:
    def __init__(self, ingredient: tuple):
        self.ingredient = ingredient[0]
        self.measure = ingredient[1]
        self.unit = ingredient[2]
    
    def __iter__(self):
        yield('ingredient', self.ingredient)
        yield('measure', self.measure)
        yield('unit', self.unit)


class recipe:
    def __init__(self, name: str, ingredients: list, garnish: list, drinkware: list, served: list, instructions, notes):
        self.name = name
        self.ingredients = []
        for i in ingredients:
            self.ingredients.append(cocktail_ingredient(i))
        self.garnish = garnish
        self.drinkware = drinkware
        self.served = served
        self.instructions = instructions if instructions is not None else ""
        self.notes = notes if notes is not None else ""
    
    # getters

    def get_name(self):
        return self.name
    
    def get_ingredients(self):
        return self.ingredients
    
    def get_garnish(self):
        return self.instructions
    
    def get_drinkware(self):
        return self.drinkware
    
    def get_served(self):
        return self.served
    
    def get_instructions(self):
        return self.instructions
    
    def get_notes(self):
        return self.notes

    # built-in overloads

    def __iter__(self):
        yield('notes', self.notes)
        yield('instructions', self.instructions)
        yield('served', self.served)
        yield('drinkware', self.drinkware)
        yield('garnish', self.garnish)
        yield('ingredients', self.ingredients)
        yield('name', self.name)

    def __str__(self):
        to_return = f"name: {self.name}\n"

        for i in self.ingredients:
            to_return += f"{i[1]} {i[2]} of {i[0]}\n"

        to_return += "Typical garnishes: "
        for i in self.garnish:
            to_return += f"{i}, "
        
        to_return += "\nServed in: "
        for i in self.drinkware:
            to_return += f"{i}"
        
        to_return += "\nServed: "
        for i in self.served:
            to_return += f"{i}"
        
        to_return += "\nInstructions: " + self.instructions + "\n"
        to_return += "Notes: " + self.notes + "\n"

        return to_return
