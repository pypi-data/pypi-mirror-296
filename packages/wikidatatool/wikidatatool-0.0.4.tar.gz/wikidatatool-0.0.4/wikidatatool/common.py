
from pandas import json_normalize
from SPARQLWrapper import JSON, SPARQLWrapper

def search_label(label, lang='en'):
    """
    Searches for entities in Wikidata that match a given label in a specified language.

    This function constructs and sends a SPARQL query to the Wikidata Query Service to find entities
    matching the provided label. The query retrieves various details about the entities including
    their descriptions, types, alternative labels, main categories, and corresponding Wikipedia articles.

    Args:
        label (str): The label to search for in Wikidata.
        lang (str): The language code for the search and the returned labels (default is 'en' for English).

    Returns:
        pandas.DataFrame: A DataFrame containing the search results with columns for article URL, 
                          item ID, item label, item description, entity types, main category, 
                          Wikipedia label, and alternative labels.

    Example:
        >>> search_wikidata_label("Albert Einstein")
        # Returns a DataFrame with information about entities related to "Albert Einstein"
    """
    sparql_query = (
        'SELECT DISTINCT ?article ?item ?itemLabel ?itemDescription '
        '(GROUP_CONCAT(DISTINCT(?entity_type); separator = ", ") AS ?entity_type_list) '
        '?main_category ?wikipediaLabel '
        '(GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {'
        'SERVICE wikibase:mwapi {'
        'bd:serviceParam wikibase:api "EntitySearch". '
        'bd:serviceParam wikibase:endpoint "www.wikidata.org".'
        f'bd:serviceParam mwapi:search "{label}".'
        f'bd:serviceParam mwapi:language "{lang}" .'
        '?item wikibase:apiOutputItem mwapi:item .'
        '?num wikibase:apiOrdinal true .}'
        '?item wdt:P31 ?entity_type .'
        'MINUS { ?item wdt:P31 wd:Q4167410}'
        'OPTIONAL { ?item wdt:P910 ?main_category}'
        'OPTIONAL { ?item skos:altLabel ?altLabel .}'
        'OPTIONAL { ?article schema:about ?item; schema:isPartOf <https://en.wikipedia.org/>; schema:name ?wikipediaLabel}'
        'SERVICE wikibase:label {'
        f'bd:serviceParam wikibase:language "{lang}" .'
        '}'
        '}'
        'GROUP BY ?article ?item ?itemLabel ?itemDescription ?main_category ?wikipediaLabel'
    )

    # URL for the Wikidata Query Service
    sparql_service_url = "https://query.wikidata.org/sparql"
    
    # Execute the query using a helper function (assumed to be defined elsewhere)
    result_table = query_wikidata(sparql_query, sparql_service_url)
    
    return result_table

def query_wikidata(sparql_query, sparql_service_url):
    """
    Queries a SPARQL endpoint with a given query and returns the results as a pandas DataFrame.

    Args:
        sparql_query (str): The SPARQL query to execute on the endpoint.
        sparql_service_url (str): The URL of the SPARQL service endpoint to query.

    Returns:
        pandas.DataFrame: A DataFrame containing the results of the SPARQL query, 
                          normalized from the JSON response format.

    Prints:
        str: The SPARQL query being executed, for debugging or logging purposes.

    Notes:
        - The function uses `SPARQLWrapper` to create the connection and specify the user agent.
        - Wikidata enforces a strict User-Agent policy, so the user agent must be explicitly set.
        - The results are returned in JSON format, which is then normalized and converted into a DataFrame.

    References:
        - https://www.wikidata.org/wiki/Wikidata:Project_chat/Archive/2019/07#problems_with_query_API
        - https://meta.wikimedia.org/wiki/User-Agent_policy
    """
    
    print(sparql_query)  # Print the query for debugging purposes
    
    # Create the connection to the SPARQL endpoint and set the user-agent
    sparql = SPARQLWrapper(sparql_service_url, agent="Sparql Wrapper on Jupyter example")
    
    sparql.setQuery(sparql_query)  # Set the SPARQL query to execute
    sparql.setReturnFormat(JSON)   # Request the result in JSON format

    # Execute the query and convert the result into a Python dictionary
    result = sparql.query().convert()
    
    # Normalize the JSON response into a pandas DataFrame
    return json_normalize(result["results"]["bindings"])


def search_alterante_label(label, lang='en'):
    """
    Queries Wikidata for an item using an alternate label and returns the results in a structured table.

    Args:
        label (str): The alternate label to search for in Wikidata.
        lang (str, optional): The language code for the label and item descriptions. Defaults to 'en' (English).

    Returns:
        pandas.DataFrame: A table containing results for the query, including article URL, item, label, description,
                          entity type list, and other related data.

    Notes:
        - The query excludes items of type 'Wikimedia disambiguation page' (wd:Q4167410).
        - The query also looks for related articles on Wikipedia in the specified language.
        - If you need to query a different SPARQL endpoint, modify the 'sparql_service_url'.
    """
    
    sparql_query = (
        'SELECT DISTINCT ?article ?item ?itemLabel ?itemDescription (GROUP_CONCAT(DISTINCT(?entity_type); separator = ", ") AS ?entity_type_list) ?main_category ?wikipediaLabel (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {'
        f'?item ?altLabel "{label}"@{lang}.'  # Use the `lang` parameter for the alternate label language

        'MINUS { ?item wdt:P31 wd:Q4167410}'

        'OPTIONAL { ?article schema:about ?item;'
        f'schema:isPartOf <https://{lang}.wikipedia.org/>;'  # Use the `lang` parameter for Wikipedia language
        'schema:name ?wikipediaLabel}'
        'OPTIONAL { ?item skos:altLabel ?altLabel .}'
        'SERVICE wikibase:label {'
        f'bd:serviceParam wikibase:language "{lang}" .'  # Use the `lang` parameter for item descriptions
        '}}'
        'GROUP BY ?article ?item ?itemLabel ?itemDescription ?main_category ?wikipediaLabel'
    )
    
    # to query another endpoint, change the URL for the service and the query
    sparql_service_url = "https://query.wikidata.org/sparql"
    result_table = query_wikidata(sparql_query, sparql_service_url)
    
    return result_table
