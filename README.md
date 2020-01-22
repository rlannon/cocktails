# cocktails
A simple full-stack app to implement a cocktail lookup tool.

## API
Included in this project is an API to find cocktails and information about them. API calls are made with GET requests and always return JSON data. The path to the API is `/api/v1/`. Additional paths are:

* `cocktail=<name>` - Get a cocktail by name '`name`'
* `ingredients=<ingredients>` - Filter cocktails by specified ingredients; multiple ingredients may be specified by concatenating with the plus sign (`+`)
* `garnish=<garnish>` - Filter cocktails by their typical garnishes. As with `ingredients`, multiple may be specified with concatenation
* `main_alcohol=<alcohol>` - Filter cocktails by their main alcohol ingredient
* `drinkware=<drinkware>` - Filter cocktails by their typical drinkware:
    * `rocks` - Drinks served in rocks/old-fashioned/lowball glasses
    * `cocktail` - Drinks served in cocktail/martini glasses
    * `highball` - Drinks served in highball glasses
    * `collins` - Drinks served in collins glasses
    * `shot` - Drinks served in a shot glass
* `served=<how served>` - Filter by how the cocktail is served:
    * `rocks` - Filter by cocktails served on the rocks (e.g., an old fashioned)
    * `straight` - Filter by cocktails served straight (e.g., a martini)
    * `blended` - Filter by blended cocktails
    * `hot` - Filter by hot cocktails (e.g., Irish Coffee)
