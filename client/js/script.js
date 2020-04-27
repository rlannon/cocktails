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

async function display_query_input(which) {
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
    let callback_function;

    // Add items based on what we are querying by
    if (which === NAME_CONST) {
        // name query
        
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
        callback_function = async function() {
            return await name_query(input_field.value);
        };
    } else if (which === INGREDIENTS_CONST) {
        // ingredient query
        // fetch ingredient list from database
        let ingredients = await get_data("/ingredients");

        // Now that we have the ingredients, send everything to our function
        input_div = display_selector_and_table("Ingredient", input_div, ingredients);

        // todo: add option for 'contains any' vs 'contains all' vs 'contains only'
        callback_function = async function() {
            let query_table = input_div.querySelector('table');
            return await ingredient_query(query_table);
        };
    } else if (which === GARNISH_CONST) {
        // garnish query
        let garnishes = await get_data("/garnish");
        input_div = display_selector_and_table("Garnish", input_div, garnishes);
        callback_function = async function() {
            let query_table = input_div.querySelector('table');
            return await garnish_query(query_table);
        };
    } else if (which === DRINKWARE_CONST) {
        // drinkware query
        let drinkware = await get_data("/drinkware");
        input_div = display_selector_and_table("Drinkware", input_div, drinkware);
        callback_function = async function() {
            let query_table = input_div.querySelector("table");
            return await drinkware_query(query_table);
        };
    } else if (which == SERVED_CONST) {
        // served query
        console.log("query by serving method");
        let served = await get_data("/served");
        input_div = display_selector_and_table("Serving Method", input_div, served);
        callback_function = async function() {
            let query_table = input_div.querySelector('table');
            return await served_query(query_table);
        };
    } else {
        // errorr; do not display anything more and log the error (this shouldn't really occur, though)
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
    query_header_text.textContent = "Cocktail Lookup";

    query_header_col.appendChild(query_header_text);
    query_header_row.appendChild(query_header_col);
    query_div.appendChild(query_header_row);

    // now, append the stuff we generated earlier
    query_div.appendChild(input_div);

    // now, append a search button
    let button_row = document.createElement("div");
    button_row.setAttribute("class", "row");
    button_row.setAttribute("id", "search-button");
    let button_col = document.createElement("div");
    button_col.setAttribute("class", "col");
    let button = document.createElement("button");
    button.setAttribute("class", "col btn btn-primary");
    button.addEventListener("click", async function() {
        // get the returned data
        let returned_data = await callback_function();
        console.log(returned_data); // log it to the console for now (for debugging)

        // use the appropriate function to display our returned data
        if (returned_data.length > 0) {
            // display returned data in a readable way
            console.log("Found recipes");
        } else {
            // display error message such as 'no recipes found'
            console.log("No recipes found");
        }
    });
    button.innerText = "Search";
    
    button_col.appendChild(button);
    button_row.appendChild(button_col);
    query_div.appendChild(button_row);
}

function display_selector_and_table(what, where, item_list) {
    /*

    display_selector_and_table
    Displays the selector for what we want to query and creates the table for it

    @param  what    A string containing the name of what we are looking up (e.g., 'Ingredient')
    @param  where   The div to which we want to append everything
    @param  item_list   The list of items to populate our selector

    */
    
    where = document.createElement("div");

    // create a div for our list
    let table_div = document.createElement("div");

    // create a list to hold our ingredients
    let selected_table = document.createElement("table");
    selected_table.setAttribute("class", "table table-bordered table-striped");
    selected_table.setAttribute("id", "selected-ingredients");
    let selected_list_header = document.createElement("thead");
    let selected_list_header_row = document.createElement("tr");
    let selected_list_header_item = document.createElement("th");
    selected_list_header_item.innerText = `${what}`;
    selected_list_header_row.appendChild(selected_list_header_item);
    selected_list_header.appendChild(selected_list_header_row);
    selected_table.appendChild(selected_list_header);
    let selected_table_body = document.createElement("tbody");
    selected_table.appendChild(selected_table_body);

    // add the table to our div
    table_div.appendChild(selected_table);

    // now add a 'clear' button
    let clear_button_div = document.createElement("div");
    clear_button_div.setAttribute("class", "row");
    let clear_button_col = document.createElement("div");
    clear_button_col.setAttribute("class", "col");
    let clear_table_button = document.createElement("button");
    clear_table_button.setAttribute("class", "btn btn-danger");
    clear_table_button.addEventListener("click", function() {clear_table(selected_table)});
    clear_table_button.innerText = "Clear table";
    clear_button_col.appendChild(clear_table_button);
    clear_button_div.appendChild(clear_button_col);

    // create a selector
    let selector_input_div = document.createElement("div");
    selector_input_div.setAttribute("class", "row");
    let selector_col = document.createElement("div");
    selector_col.setAttribute("class", "col input-group");

    // create the selector input
    let selector = document.createElement("select");
    selector.setAttribute("class", "custom-select");
    let default_element = document.createElement("option");
    default_element.setAttribute("value", "None");
    default_element.innerText = "Select...";
    selector.appendChild(default_element);
    for (let ingredient of item_list) {
        let option = document.createElement("option");
        option.setAttribute("value", ingredient);
        option.innerText = ingredient;
        selector.appendChild(option);
    }

    // create the button
    let add_button_div = document.createElement("div");
    add_button_div.setAttribute("class", "input-group-append");
    let add_button = document.createElement("button");
    add_button.setAttribute("class", "btn btn-outline-secondary");
    add_button.addEventListener("click", function() { add_to_table(selector, selected_table_body) });
    add_button.innerText = `Add ${what}`;
    add_button_div.appendChild(add_button);

    // add the selector and button to the input
    selector_col.appendChild(selector);
    selector_col.appendChild(add_button_div);

    // construct the input div
    selector_input_div.appendChild(selector_col);
    where.appendChild(selector_input_div);
    where.appendChild(table_div);
    where.appendChild(clear_button_div);

    // finally, return the generated content
    return where;
}

function add_to_table(selector, table) {
    /*

    add_to_table
    Adds the selected element from 'selector' to 'table'

    */
    let selected = selector.options[selector.selectedIndex].value;
    if (selected === "None") {
        console.log("Skipping");
    } else {
        console.log("Add '" + selected + "' to table");
        let table_item = document.createElement("tr");
        let table_col = document.createElement("td");
        table_col.innerText = selected;
        table_item.appendChild(table_col);
        table.appendChild(table_item);
    }
}

function clear_table(table) {
    // Clears a table of all table rows
    let old_tbody = table.querySelector("tbody");
    while(old_tbody.firstChild) {
        old_tbody.removeChild(old_tbody.lastChild);
    }
}
