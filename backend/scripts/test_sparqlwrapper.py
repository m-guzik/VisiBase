import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from wikibaseintegrator.wbi_helpers import execute_sparql_query

endpoint_url = "https://lexbib.elex.is/query/sparql"

query = """SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
                        ?property1 <https://lexbib.elex.is/prop/direct/P95> ?property2 .
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
                        }"""

def get_results(endpoint_url, query):
    user_agent = "SPARQL Wrapper App"
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.addCustomHttpHeader("User-Agent", "SPARQL Wrapper App")
    sparql.addCustomHttpHeader("Accept", "application/sparql-results+json")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)