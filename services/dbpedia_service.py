from SPARQLWrapper import SPARQLWrapper, JSON
from utils.query_builder import build_search_query, build_relation_query

class DBPediaService:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self.sparql.setReturnFormat(JSON)

    def search_movies(self, search_term):
        """Search for movies by title or description."""
        query = build_search_query(search_term, entity_type="http://dbpedia.org/ontology/Film")
        self.sparql.setQuery(query)

        try:
            results = self.sparql.query().convert()
            print(results)  # Debugging: Print raw results to verify structure
            return [
                {
                    "uri": result["entity"]["value"],
                    "label": result["label"]["value"],
                    "description": result["description"]["value"]
                }
                for result in results["results"]["bindings"]
            ]
        except KeyError as e:
            raise Exception(f"Missing key in SPARQL result: {str(e)}")
        except Exception as e:
            raise Exception(f"Error querying DBPedia: {str(e)}")

    def fetch_movie_relations(self, movie_uri):
        """Fetch relations (actors, director, producer) for a given movie."""
        query = build_relation_query(movie_uri)
        self.sparql.setQuery(query)

        try:
            results = self.sparql.query().convert()
            return [
                {
                    "relation": result["relation"]["value"],
                    "entity": result["related_entity"]["value"],
                    "label": result["label"]["value"]
                }
                for result in results["results"]["bindings"]
            ]
        except Exception as e:
            raise Exception(f"Error fetching movie relations: {str(e)}")
