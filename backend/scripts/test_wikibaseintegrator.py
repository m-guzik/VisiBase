from wikibaseintegrator.wbi_helpers import execute_sparql_query
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator import WikibaseIntegrator
import requests

session = requests.Session()

session.headers.update({
    'User-Agent': 'VisiBase/1.0 (https://example.org)',
    'Accept': 'application/json'  # optional but useful
})

wbi_config['SESSION'] = session
wbi_config['SPARQL_ENDPOINT_URL'] = 'https://lexbib.elex.is/query/sparql'
wbi = WikibaseIntegrator()



query = """
PREFIX wdt: <https://lexbib.elex.is/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
    ?property1 wdt:P95 ?property2 .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
}
"""

results = execute_sparql_query(query)

for result in results["results"]["bindings"]:
    print(result)