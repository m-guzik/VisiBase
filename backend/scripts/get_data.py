import requests

from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.wbi_helpers import execute_sparql_query



def get_classes(request_id: str):
    match request_id:
        case "lexbib":
            print("tu")
            wbi_config['MEDIAWIKI_API_URL'] = 'https://lexbib.elex.is/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://lexbib.elex.is/query/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://lexbib.elex.is' 
            PID_INSTANCE_0F = "ldp:P5" 
            PREFIX = "PREFIX ldp: <https://lexbib.elex.is/prop/direct/>" 
        case "wikibase-world":
            print("teraz tu")
            wbi_config['MEDIAWIKI_API_URL'] = 'https://wikibase.world/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://wikibase.world/query/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://wikibase.world' 
            PID_INSTANCE_0F = "wwdt:P3" 
            PREFIX = " PREFIX wwdt: <https://wikibase.world/prop/direct/> "  
        case "wikihum":
            print("a teraz tu")
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
