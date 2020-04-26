/*

Cocktails
api_access.js
Copyright 2020 Riley Lannon

API access functions

*/

// API URL constant
const API_URL = "http://localhost:5000/api/v1"   // since it's locally hosted for now, use localhost

async function get_data(url)
{
    /*

    get_data
    Fetches data from an API and returns JSON objects

    @param  url The API path we are fetching data from

    */
    
    url = API_URL + url;    // add the API path to the end of the API url

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
