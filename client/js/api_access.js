/*

Cocktails
api_access.js
Copyright 2020 Riley Lannon

API access functions

*/

async function get_data(url)
{
    /*

    get_data
    Fetches data from an API and returns JSON objects

    @param  url The URL we are fetching data from

    */

    return fetch(url)
        .then(response => response.json())
        .catch(error => console.log(error));
}

async function drinkware_query()
{
    /*

    drinkware_query
    Formulates a drinkware query

    */
}
