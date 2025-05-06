from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.wbi_helpers import execute_sparql_query

from SPARQLWrapper import SPARQLWrapper, JSON

import requests




def get_classes(request_id: str):
    match request_id:
        case "factgrid":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://database.factgrid.de/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://database.factgrid.de/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://database.factgrid.de' 
            PID_INSTANCE_0F = " wdt:P2" 
            PREFIX = "  "  
        case "lexbib":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://lexbib.elex.is/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://lexbib.elex.is/query/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://lexbib.elex.is' 
            PID_INSTANCE_0F = "ldp:P5" 
            PREFIX = "PREFIX ldp: <https://lexbib.elex.is/prop/direct/>" 
        case "qichwabase":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://qichwa.wikibase.cloud/w/api.php'
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://qichwa.wikibase.cloud/query/sparql'
            wbi_config['WIKIBASE_URL'] = 'https://qichwa.wikibase.cloud'
            PID_INSTANCE_0F = "<https://qichwa.wikibase.cloud/prop/direct/P5>" 
            PREFIX = " "
        case "kul":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://va.wiki.kul.pl/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://va.wiki.kul.pl/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://va.wiki.kul.pl' 
            PID_INSTANCE_0F = "wdt:P1" 
            PREFIX = " "
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
        # case "wikikul":
        #     wbi_config['MEDIAWIKI_API_URL'] = 'https://wiki.kul.pl/w/api.php' 
        #     wbi_config['SPARQL_ENDPOINT_URL'] = 'https://wiki.kul.pl/sparql' 
        #     wbi_config['WIKIBASE_URL'] = 'https://wiki.kul.pl' 
        #     PID_INSTANCE_0F = "wdt:P1" 
        #     PREFIX = " "

    query =  PREFIX + """
                SELECT DISTINCT ?instance ?instanceLabel WHERE {
                    ?item """ + PID_INSTANCE_0F + """ ?instance .
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }
                """

    results = execute_sparql_query(query)
    classes = []
    for result in results["results"]["bindings"]:
        class_link =result["instance"]["value"]
        class_id = result["instance"]["value"].split("/")[-1]
        class_number = int(class_id[1:]) 
        class_label = result["instanceLabel"]["value"]
        instance_class = { "link" : class_link, 
                "id" : class_id,
                "number" : class_number,
                "label" : class_label }
        classes.append(instance_class)

    return classes





def get_properties(sparql_endpoint: str, wiki_url: str):
    query = """
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX bd: <http://www.bigdata.com/rdf#>

        SELECT ?property ?propertyLabel ?datatype WHERE {
                    ?property a wikibase:Property ;
                                wikibase:propertyType ?datatype .
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
                }
        """

    headers = {
        "User-Agent": "WikibaseIntegrator/0.11 (https://github.com/LeMyst/WikibaseIntegrator)",
        "Accept": "application/sparql-results+json"
    }

    response = requests.get(sparql_endpoint, params={"query": query}, headers=headers)

    properties = []
    connected_properties = []

    nodes = []
    edges = []
    node_ids = set()

    if response.status_code == 200:
        data = response.json()
        for result in data["results"]["bindings"]:
            property_link =result["property"]["value"]
            property_id = result["property"]["value"].split("/")[-1]
            property_number = int(property_id[1:]) 
            property_label = result["propertyLabel"]["value"]
            property_datatype = result["datatype"]["value"].split("#")[-1]
            prop = { "link" : property_link, 
                    "id" : property_id,
                    "number" : property_number,
                    "label" : property_label,
                    "datatype" : property_datatype }
            properties.append(prop)

            if property_datatype == "WikibaseProperty":
                WDT_PREFIX = "<" + wiki_url + "/prop/direct/>"
                query = """
                PREFIX wdt: """ + WDT_PREFIX + """
                PREFIX wikibase: <http://wikiba.se/ontology#>
                PREFIX bd: <http://www.bigdata.com/rdf#>

                SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
                    ?property1 wdt:""" + property_id + """ ?property2 .
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
                }
                """

                headers = {
                    "User-Agent": "WikibaseIntegrator/0.11 (https://github.com/LeMyst/WikibaseIntegrator)",
                    "Accept": "application/sparql-results+json"
                }

                response = requests.get(sparql_endpoint, params={"query": query}, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    connecting_property = { 'id': property_id, 'link': property_link, 'label': property_label, 'connections': [] }
                    for result in data["results"]["bindings"]:
                        from_property_link = result["property1"]["value"]
                        from_property_id = result["property1"]["value"].split("/")[-1]
                        from_property_label = result["property1Label"]["value"]
                        to_property_link = result["property2"]["value"]
                        to_property_id = result["property2"]["value"].split("/")[-1]
                        to_property_label = result["property2Label"]["value"]
                        edge_property_id = from_property_id + property_id + to_property_id

                        if from_property_id.startswith('P') and to_property_id.startswith('P'):
                            connection = { 'from_link': from_property_link, 'from_id': from_property_id, 'from_label': from_property_label,
                                            'to_link': to_property_link, 'to_id': to_property_id, 'to_label': to_property_label }
                            connecting_property["connections"].append(connection)
                            if from_property_id not in node_ids:
                                nodes.append({
                                'id': from_property_id,
                                'label': from_property_label,
                                'link': from_property_link, 
                                'entityType': 'class'})
                                node_ids.add(from_property_id)
                            if to_property_id not in node_ids:
                                nodes.append({
                                    'id': to_property_id,
                                    'label': to_property_label,
                                    'link': to_property_link, 
                                    'entityType': 'class'})
                                node_ids.add(to_property_id)
                            
                            edges.append({
                                'id': edge_property_id,
                                'sourceId': from_property_id,
                                'targetId': to_property_id,
                                'label': property_label,
                                'entityType': 'property'})

                    if len(connecting_property["connections"]) > 0:
                        connected_properties.append(connecting_property)
                else:
                    print("Query failed:", response.status_code, response.text)
    else:
        print("Query failed:", response.status_code, response.text)




    # user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # sparql = SPARQLWrapper(sparql_endpoint, agent=user_agent)

    # sparql.setQuery("""
    #             SELECT ?property ?propertyLabel ?datatype WHERE {
    #                 ?property a wikibase:Property ;
    #                             wikibase:propertyType ?datatype .
    #                 SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
    #             } """)
    # sparql.setReturnFormat(JSON)
    # results = sparql.query().convert()

    # properties = []
    # connected_properties = []

    # for result in results["results"]["bindings"]:
    #     property_link =result["property"]["value"]
    #     property_id = result["property"]["value"].split("/")[-1]
    #     property_number = int(property_id[1:]) 
    #     property_label = result["propertyLabel"]["value"]
    #     property_datatype = result["datatype"]["value"].split("#")[-1]
    #     prop = { "link" : property_link, 
    #             "id" : property_id,
    #             "number" : property_number,
    #             "label" : property_label,
    #             "datatype" : property_datatype }
    #     properties.append(prop)
    #     if property_datatype == "WikibaseProperty":
    #         PROPERTY_ID = "<" + wiki_url + "/prop/direct/" + property_id + ">"
    #         print("Property ID with prefix ", PROPERTY_ID)

    #         query =  """
    #                      SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
    #                      ?property1 """ + PROPERTY_ID + """ ?property2 .
    #                      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
    #                      } """
    #         results = execute_sparql_query(query)
    #         # sparql.setQuery("""
    #         #             SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
    #         #             ?property1 """ + PROPERTY_ID + """ ?property2 .
    #         #             SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
    #         #             } """)
    #         # sparql.setReturnFormat(JSON)
    #         # results = sparql.query().convert()
    #         connecting_property = { 'id': property_id, 'link': property_link, 'label': property_label, 'connections': [] }
    #         for result in results["results"]["bindings"]:
    #             message = f"{result["property1"]["value"]} ↔ {result["property2"]["value"]}"
    #             print(message)
    #             from_property_link = result["property1"]["value"]
    #             from_property_id = result["property1"]["value"].split("/")[-1]
    #             from_property_label = result["property1Label"]["value"]
    #             to_property_link = result["property2"]["value"]
    #             to_property_id = result["property2"]["value"].split("/")[-1]
    #             to_property_label = result["property2Label"]["value"]

    #             if from_property_id.startswith('P') and to_property_id.startswith('P'):
    #                 connection = { 'from_link': from_property_link, 'from_id': from_property_id, 'from_label': from_property_label,
    #                                 'to_link': to_property_link, 'to_id': to_property_id, 'to_label': to_property_label }
    #                 connecting_property["connections"].append(connection)
    #         if len(connecting_property["connections"]) > 0:
    #             connected_properties.append(connecting_property)

    return properties, connected_properties, edges, nodes

