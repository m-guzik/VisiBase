import requests

endpoint = "https://lexbib.elex.is/query/sparql"

query = """
PREFIX wdt: <https://lexbib.elex.is/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>

SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
    ?property1 wdt:P95 ?property2 .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
}
"""

headers = {
    "User-Agent": "WikibaseIntegrator/0.11 (https://github.com/LeMyst/WikibaseIntegrator)",
    "Accept": "application/sparql-results+json"
}

response = requests.get(endpoint, params={"query": query}, headers=headers)

if response.status_code == 200:
    data = response.json()
    for result in data["results"]["bindings"]:
        print(result)
else:
    print("Query failed:", response.status_code, response.text)