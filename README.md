# cocktails

A simple full-stack app to implement a cocktail lookup tool.

## Getting Started

### Database

Included in this project is a folder of CSV files and some SQL for creating and populating a PostgreSQL database. I also intend on hosting this API, though there is not currently a working cloud application.

### Server

The server-side application utilizes [Flask](https://flask.palletsprojects.com/en/1.1.x/), a server-side framework for Python. All information regarding database connection is expected to be contained within a `.flaskenv` file which is not included in this repository -- you must supply one yourself if you intend on building/hosting this somehwere.

While this project has a few Jinja templates, the server is not intended to host the actual web app itself -- rather, that is the client's job. The server-side templates contain some information about the API and use a flask markdown rendering library to accomplish this.

All required libraries can be found in the [requirements](requirements.txt)

### Client

The client-side code implements a simple web app that actually utilizes the API.

## API

Included in this project is an API to find cocktails and information about them. API calls are made with GET requests and always return JSON data. The base path to the API is `/api/v1/`.

### JSON Objects

The JSON Objects returned by this API contain the following fields:

* `name` - The name of the cocktail
* `ingredients` - A list of ingredients in the cocktail, each entry containing the following information:
    * `name` - The name of the ingredient
    * `measure` - The measure number of said ingredient
    * `unit` - The unit of said measurement
    * **NB:** For measurements like 'to taste', `measure` will be `1` and `unit` will indicate whether it is to taste, etc.
* `garnish` - A list of strings containing common garnishes served with the cocktail
* `drinkware` - A list of strings containing the drinkware the cocktail is most commonly served in
* `served` - How this cocktail is normally served (on the rocks, blended, etc)
* `instructions` - Any special instructions for the cocktail's preparation
* `notes` - Any miscellaneous notes about the cocktail

### Paths

Paths supported by this API are:

* `cocktail/<name>` or `name/<name>`- Get a cocktail by name
* `ingredients` - List ingredients in the database
* `ingredients/<ingredients>` - Lists cocktails containing any of the specified ingredients; ingredients may be concatenated with the plus sign (`+`)
* `contains/<ingredients>` - Filter by cocktails that contain all of the specified ingredients; concatenation with the plus sign is supported
* `garnish` - List garnishes in the database
* `garnish/<garnish>` - Filter cocktails by their typical garnishes. As with `ingredients` and `contains`, multiple may be specified with concatenation
* `drinkware` - List all drinkware in the database
* `drinkware/<drinkware>` - Filter cocktails by their typical drinkware:
    * `old fashioned glass` or `rocks glass` or `old fashioned` or `lowball` - Drinks served in rocks/old-fashioned/lowball glasses
    * `cocktail glass` - Drinks served in cocktail/martini glasses
    * `highball glass` - Drinks served in highball glasses
    * `collins glass` - Drinks served in collins glasses
    * `shot glass` - Drinks served in a shot glass
    * `hurricane glass` - Drinks served in hurricane glasses
    * `coupe glass` - Drinks served in coupe glasses
* `served/<how served>` - Filter by how the cocktail is served:
    * `on the rocks` or `iced` - Filter by cocktails served on the rocks (e.g., an old fashioned)
    * `straight up` - Filter by cocktails served straight/up/straight up (e.g., a martini)
    * `neat` - Filter by drinks served neat
    * `blended` - Filter by blended and frozen cocktails (e.g., a piña colada)
    * `hot` - Filter by hot cocktails (e.g., Irish coffee)

You may also use a combination of the above paths as named parameters by using `/api/v1/custom` followed by URL parameters. For example:

    .../api/v1/custom?ingredients=vodka&drinkware=old-fashioned&served=straight

will search for cocktails which contain vodka, which are served in an old-fashioned glass, and which are served straight.


### Naming Conventions

The strings you supply to the API will be normalized, where possible, to what the database expects. For example, the database uses the spelling 'whiskey', but 'whisky' is another common spelling; as such, if you try to look up by ingredient and use a common alternate spelling, it will be normalized to the spelling used by the database. This is done by maintaining a table of common spellings/terms and what their equivalent term (as used by the database) is.

### Cocktail list

Note this tool isn't currently meant to be anything even remotely resembling a complete list of all the cocktails one might want to make; the included CSV files are just a sampling of a few different common cocktails using a variety of drinkware, ingredients, garnishes, and serving methods. The CSV folder is meant to be used to populate a database with a few different drinks to demo its functionality.
