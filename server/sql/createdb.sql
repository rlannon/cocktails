-- createdb.sql
-- Contains all the statements needed to create our database tables

-- recipe
-- contains information about individual recipes
CREATE TABLE recipe(
    id SERIAL NOT NULL,
    name VARCHAR(50),
    instructions VARCHAR(250),
    notes VARCHAR(250)
);

-- ingredients
-- contains information about each individual ingredient
CREATE TABLE ingredients (
    ingredient_id SERIAL NOT NULL,
    name VARCHAR(50)
);

-- cocktail_ingredient
-- contains information about ingredients, associated with 'recipe' by the recipe_id field
CREATE TABLE cocktail_ingredient (
    recipe_id INTEGER,
    ingredient_id INTEGER,
    measure_number FLOAT,
    unit_of_measurement VARCHAR(10)
);

-- drinkware
-- contains information about each drinkware item
CREATE TABLE drinkware (
    drinkware_id SERIAL NOT NULL,
    name VARCHAR(50)
);

-- cocktail_drinkware
-- contains associations between drinkware and ingredients
CREATE TABLE cocktail_drinkware (
    recipe_id INTEGER,
    drinkware_id INTEGER
);

-- garnish
-- contains information about garnishes
CREATE TABLE garnish (
    garnish_id SERIAL NOT NULL,
    name VARCHAR(50)
);

-- cocktail_garnish
-- contains associations between cocktails and garnishes
CREATE TABLE cocktail_garnish (
    recipe_id INTEGER,
    garnish_id INTEGER
);

-- served
-- information about serving methods
CREATE TABLE served (
    served_id SERIAL NOT NULL,
    name VARCHAR(20)
);

-- cocktail_served
-- associations between cocktail serving methods and their recipes
CREATE TABLE cocktail_served (
    recipe_id INTEGER,
    served_id INTEGER
);

-- normalize
-- a normalization table to convert user input into expected database input
-- contains other common names for various data from the db
CREATE TABLE normalize (
    db_name VARCHAR(50),
    supplied_name VARCHAR(50)
);
