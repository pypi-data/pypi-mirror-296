
from pandas import json_normalize
from SPARQLWrapper import JSON, SPARQLWrapper

def build_sparql_query(label, lang='en', is_alt_label=False):
    """
    Constructs the SPARQL query for searching by label or alternate label.

    Args:
        label (str): The label to search for.
        lang (str): The language code for the search and returned labels (default 'en').
        is_alt_label (bool): If True, search using the alternate label. Otherwise, search by the main label.

    Returns:
        str: The constructed SPARQL query.
    """
    label_clause = (
        f'?item ?altLabel "{label}"@{lang}.' if is_alt_label else
        f'bd:serviceParam mwapi:search "{label}"; bd:serviceParam mwapi:language "{lang}".'
    )

    query = (
        'SELECT DISTINCT ?article ?item ?itemLabel ?itemDescription '
        '(GROUP_CONCAT(DISTINCT(?entity_type); separator = ", ") AS ?entity_type_list) '
        '?main_category ?wikipediaLabel '
        '(GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {'
        f'SERVICE wikibase:mwapi {{ {label_clause} }}' if not is_alt_label else f'{label_clause}'
        '?item wdt:P31 ?entity_type .'
        'MINUS { ?item wdt:P31 wd:Q4167410}'
        'OPTIONAL { ?item wdt:P910 ?main_category}'
        'OPTIONAL { ?item skos:altLabel ?altLabel .}'
        f'OPTIONAL {{ ?article schema:about ?item; schema:isPartOf <https://{lang}.wikipedia.org/>; schema:name ?wikipediaLabel}}'
        'SERVICE wikibase:label {'
        f'bd:serviceParam wikibase:language "{lang}" .}}'
        'GROUP BY ?article ?item ?itemLabel ?itemDescription ?main_category ?wikipediaLabel'
    )
    
    return query

# Use the helper function to refactor both search functions
def search_label(label, lang='en'):
    query = build_sparql_query(label, lang, is_alt_label=False)
    return query_wikidata(query, "https://query.wikidata.org/sparql")

def search_alternate_label(label, lang='en'):
    query = build_sparql_query(label, lang, is_alt_label=True)
    return query_wikidata(query, "https://query.wikidata.org/sparql")
