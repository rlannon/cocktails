/*

Cocktails
script.js
Copyright 2020 Riley Lannon

Basic scripts for the cocktail tool
api_access.js is included before this file, so we can utilize its functions here


*/

const NAME_CONST = 1;
const INGREDIENTS_CONST = 2;
const GARNISH_CONST = 3;
const DRINKWARE_CONST = 4;
const SERVED_CONST = 5;

function display_query_input(which) {
    /*

    display_query_input
    Displays the input form to formulate a query to our API based on what the user wishes to get

    @param  which   Which query form to display; should be one of the constants declared above

    */
    
    if (which === NAME_CONST) {
        // name query
    } else if (which === INGREDIENTS_CONST) {
        // ingredient query
    } else if (which === GARNISH_CONST) {
        // garnish query
    } else if (which === DRINKWARE_CONST) {
        // drinkware query
    } else if (which == SERVED_CONST) {
        // served query
    } else {
        // errorr; do not display anything more and log the error
        console.log("Invalid parameter")
    }
}
