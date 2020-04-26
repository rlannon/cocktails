/*  jshint esversion: 8 */
"use strict";

/*

Cocktails
script.js
Copyright 2020 Riley Lannon

Basic scripts for the cocktail tool
api_access.js is included before this file, so we can utilize its functions here


*/

// Some constants for our query input function
const NAME_CONST = 1;
const INGREDIENTS_CONST = 2;
const GARNISH_CONST = 3;
const DRINKWARE_CONST = 4;
const SERVED_CONST = 5;

// todo: fetch ingredients, drinkware, served, garnish from the database and store them somewhere so we can use them to populate the data tables
// todo: consider - should this be done in the function (calling the API each time), or when the script is loaded (and then just use client-side data)?

function display_query_input(which) {
    /*

    display_query_input
    Displays the input form to formulate a query to our API based on what the user wishes to get

    @param  which   Which query form to display; should be one of the constants declared above

    */

    // Select the element and clear all of its child nodes
    let query_div = document.querySelector("#query");
    while (query_div.firstChild) {
        query_div.removeChild(query_div.lastChild);
    }

    let input_div;

    // Add items based on what we are querying by
    if (which === NAME_CONST) {
        // name query
        console.log("query by name");
        
        // input row
        let input_row = document.createElement("div");
        input_row.setAttribute("class", "row");

        // create child nodes
        let input_col = document.createElement("div");
        input_col.setAttribute("class", "col input-group");
        let name_div = document.createElement("div");
        name_div.setAttribute("class", "input-group-prepend");
        let name_span = document.createElement("span");
        name_span.setAttribute("class", "input-group-text");
        name_span.innerText = "Name";
        let input_field = document.createElement("input");
        input_field.setAttribute("type", "text");
        input_field.setAttribute("class", "form-control");

        // append them
        name_div.appendChild(name_span);
        input_col.appendChild(name_div);
        input_col.appendChild(input_field);
        input_row.appendChild(input_col);

        // append the whole input to our query div
        input_div = input_row;
    } else if (which === INGREDIENTS_CONST) {
        // ingredient query
        console.log("query by ingredients");
    } else if (which === GARNISH_CONST) {
        // garnish query
        console.log("query by garnish");
    } else if (which === DRINKWARE_CONST) {
        // drinkware query
        console.log("query by drinkware");
    } else if (which == SERVED_CONST) {
        // served query
        console.log("query by serving method");
    } else {
        // errorr; do not display anything more and log the error
        console.log("Invalid parameter");
        return;
    }

    // add a row for our header

    // Create the header for our query
    let query_header_row = document.createElement("div");
    query_header_row.setAttribute("class", "row");
    
    let query_header_col = document.createElement("div");
    query_header_col.setAttribute("class", "col");

    let query_header_text = document.createElement("h3");
    query_header_text.setAttribute("class", "alert alert-secondary text-center");
    query_header_text.textContent = "Look Up Cocktail";

    query_header_col.appendChild(query_header_text);
    query_header_row.appendChild(query_header_col);
    query_div.appendChild(query_header_row);

    // now, append the stuff we generated earlier
    query_div.appendChild(input_div);

    // now, append a search button
    let button_row = document.createElement("div");
    button_row.setAttribute("class", "row");
    let button_col = document.createElement("div");
    button_col.setAttribute("class", "col");
    let button = document.createElement("button");
    button.setAttribute("class", "btn btn-primary");
    button.setAttribute("onclick", `console.log("querying...");`);  // todo: dispatch to function
    button.innerText = "Search";
    
    button_col.appendChild(button);
    button_row.appendChild(button_col);
    query_div.appendChild(button_row);
}
