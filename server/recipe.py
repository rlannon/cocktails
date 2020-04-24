# Cocktails API
# recipe.py
# Copyright 2020 Riley Lannon

# Contains a class to hold cocktail recipes

class recipe:
    def __init__(self, name: str, ingredients: list, garnish: list, drinkware: list, served: list, instructions: str, notes: str):
        self.name = name
        self.ingredients = ingredients  # tuples containing (name, measurement, unit)
        self.garnish = garnish
        self.drinkware = drinkware
        self.served = served
        self.instructions = instructions
        self.notes = notes
    
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
        "Notes: " + self.notes + "\n"

        return to_return
