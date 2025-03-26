import requests

from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.wbi_helpers import execute_sparql_query

from SPARQLWrapper import SPARQLWrapper, JSON




def get_classes(request_id: str):
    match request_id:
        case "lexbib":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://lexbib.elex.is/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://lexbib.elex.is/query/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://lexbib.elex.is' 
            PID_INSTANCE_0F = "ldp:P5" 
            PREFIX = "PREFIX ldp: <https://lexbib.elex.is/prop/direct/>" 
        case "wikibase-world":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://wikibase.world/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://wikibase.world/query/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://wikibase.world' 
            PID_INSTANCE_0F = "wwdt:P3" 
            PREFIX = " PREFIX wwdt: <https://wikibase.world/prop/direct/> "  
        case "wikihum":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://wikihum.lab.dariah.pl/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://wikihum.lab.dariah.pl/bigdata/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://wikihum.lab.dariah.pl' 
            PID_INSTANCE_0F = "wdt:P27" 
            PREFIX = " "

    query =  PREFIX + """
                SELECT DISTINCT ?instance ?instanceLabel WHERE {
                    ?item """ + PID_INSTANCE_0F + """ ?instance .
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }
                """

    results = execute_sparql_query(query)
    output = []
    labels = []
    for result in results["results"]["bindings"]:
        output.append(result["instance"]["value"])
        labels.append(result["instanceLabel"]["value"])

    # wbi = WikibaseIntegrator()

    # for item_link in output:
    #     position = item_link.rfind(r'/')
    #     item_id = item_link[position+1:]
    #     print(item_id)

    #     item = wbi.item.get(entity_id=item_id)

    #     print(item.labels.get('en'))
    #     print(item.descriptions.get('en'), '\n')

    return labels






def get_properties(request_id: str):
    match request_id:
        case "lexbib":
            sparql = SPARQLWrapper('https://lexbib.elex.is/query/sparql')
            wiki_url = 'https://lexbib.elex.is' 
        case "wikibase-world":
            sparql = SPARQLWrapper('https://wikibase.world/query/sparql')
            wiki_url = 'https://wikibase.world' 
        case "wikihum":
            sparql = SPARQLWrapper('https://wikihum.lab.dariah.pl/bigdata/sparql')
            wiki_url = 'https://wikihum.lab.dariah.pl' 


    sparql.setQuery("""
                SELECT ?property ?propertyLabel ?datatype WHERE {
                    ?property a wikibase:Property ;
                                wikibase:propertyType ?datatype .
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
                } """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    properties = []

    for result in results["results"]["bindings"]:
        prop_id = result["property"]["value"].split("/")[-1]
        label = result["propertyLabel"]["value"]
        datatype = result["datatype"]["value"].split("#")[-1]
        print(f"{prop_id}: {label} ({datatype})")
        properties.append(label)

    return properties






# # FactGrid
# wbi_config['MEDIAWIKI_API_URL'] = 'https://database.factgrid.de/w/api.php' 
# wbi_config['SPARQL_ENDPOINT_URL'] = 'https://database.factgrid.de/query/' 
# wbi_config['WIKIBASE_URL'] = 'https://database.factgrid.de' 
# PID_INSTANCE_0F = " wdt:P2" 
# PREFIX = "  "    

                     
#  wbi_config['MEDIAWIKI_API_URL'] = '' 
# wbi_config['SPARQL_ENDPOINT_URL'] = ''
#  wbi_config['WIKIBASE_URL'] = '' 
# PID_INSTANCE_0F = " " 
# PREFIX = "  "  
