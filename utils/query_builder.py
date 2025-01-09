import re

def build_search_query(search_term, entity_type=None):
    """
    Construct a SPARQL query to search for entities by title or description.
    :param search_term: The search term to query.
    :param entity_type: Optional. The RDF type to filter results (e.g., dbo:Film).
    :return: SPARQL query string.
    """
    # Escape the search term for SPARQL
    sanitized_term = re.sub(r'(["\\])', r'\\\1', search_term)

    # Basic filters for labels and descriptions
    regex_filter = f'REGEX(?label, "{sanitized_term}", "i") || REGEX(?description, "{sanitized_term}", "i")'

    # Entity type condition (only if provided)
    type_filter = f'?entity a <{entity_type}> .' if entity_type else ''

    # Combine filters and conditions
    filter_clause = f"""
        {type_filter}
        FILTER (LANG(?label) = "en" && LANG(?description) = "en")
        FILTER ({regex_filter})
    """.strip()

    # Construct the SPARQL query
    return f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT DISTINCT ?entity ?label ?description
        WHERE {{
            ?entity rdfs:label ?label ;
                   dbo:abstract ?description .
            {filter_clause}
        }}
        LIMIT 50
    """


def build_relation_query(movie_uri):
    """
    Construct a SPARQL query to fetch relationships for a movie.
    :param movie_uri: The URI of the movie.
    :return: SPARQL query string.
    """
    return f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?relation ?related_entity ?label
        WHERE {{
            {{
                <{movie_uri}> dbo:starring ?related_entity .
                ?related_entity rdfs:label ?label .
                BIND("Actor" AS ?relation)
            }}
            UNION
            {{
                <{movie_uri}> dbo:director ?related_entity .
                ?related_entity rdfs:label ?label .
                BIND("Director" AS ?relation)
            }}
            UNION
            {{
                <{movie_uri}> dbo:producer ?related_entity .
                ?related_entity rdfs:label ?label .
                BIND("Producer" AS ?relation)
            }}
            FILTER (LANG(?label) = "en")
        }}
    """