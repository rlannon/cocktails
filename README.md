# cocktails

A simple full-stack app to implement a cocktail lookup tool.

## API

Included in this project is an API to find cocktails and information about them. API calls are made with GET requests and always return JSON data. The path to the API is `/api/v1/`.

### Paths

Additional paths are:

* `cocktail=<name>` - Get a cocktail by name
* `ingredients=<ingredients>` - Filter cocktails by specified ingredients; multiple ingredients may be specified by concatenating with the plus sign (`+`)
* `garnish=<garnish>` - Filter cocktails by their typical garnishes. As with `ingredients`, multiple may be specified with concatenation
* `main_alcohol=<alcohol>` - Filter cocktails by their main alcohol ingredient
* `drinkware=<drinkware>` - Filter cocktails by their typical drinkware:
    * `rocks` - Drinks served in rocks/old-fashioned/lowball glasses
    * `cocktail` - Drinks served in cocktail/martini glasses
    * `highball` - Drinks served in highball glasses
    * `collins` - Drinks served in collins glasses
    * `shot` - Drinks served in a shot glass
    * `hurricane` - Drinks served in hurricane glasses
    * `coupe` - Drinks served in coupe glasses
* `served=<how served>` - Filter by how the cocktail is served:
    * `rocks` - Filter by cocktails served on the rocks (e.g., an old fashioned)
    * `straight` - Filter by cocktails served straight (e.g., a martini)
    * `blended` - Filter by blended and frozen cocktails (e.g., a piña colada)
    * `hot` - Filter by hot cocktails (e.g., Irish coffee)

### Cocktail list

Note this tool isn't currently meant to be a complete list of all the cocktails one might want to make; the included CSV file is just a sampling of a few different common cocktails using a variety of drinkware, ingredients, garnishes, and serving methods. The CSV is meant to be used to populate a database.
