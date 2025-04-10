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
        case "factgrid":
            wbi_config['MEDIAWIKI_API_URL'] = 'https://database.factgrid.de/w/api.php' 
            wbi_config['SPARQL_ENDPOINT_URL'] = 'https://database.factgrid.de/sparql' 
            wbi_config['WIKIBASE_URL'] = 'https://database.factgrid.de' 
            PID_INSTANCE_0F = " wdt:P2" 
            PREFIX = "  "  

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





def get_properties(request_id: str):
    match request_id:
        case "lexbib":
            sparql = SPARQLWrapper('https://lexbib.elex.is/query/sparql')
        case "wikibase-world":
            sparql = SPARQLWrapper('https://wikibase.world/query/sparql')
        case "wikihum":
            sparql = SPARQLWrapper('https://wikihum.lab.dariah.pl/bigdata/namespace/wdq/sparql')
        case "factgrid":
            sparql = SPARQLWrapper('https://database.factgrid.de/sparql')

    sparql.setQuery("""
                SELECT ?property ?propertyLabel ?datatype WHERE {
                    ?property a wikibase:Property ;
                                wikibase:propertyType ?datatype .
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
                } """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    properties = []
    connected_properties = []

    for result in results["results"]["bindings"]:
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
            PROPERTY_ID = "wdt:" + property_id
            sparql.setQuery("""
                        SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
                        ?property1 """ + PROPERTY_ID + """ ?property2 .
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
                        } """)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            connecting_property = { 'id': property_id, 'link': property_link, 'label': property_label, 'connections': [] }
            for result in results["results"]["bindings"]:
                message = f"{result["property1"]["value"]} ↔ {result["property2"]["value"]}"
                from_property_link = result["property1"]["value"]
                from_property_id = result["property1"]["value"].split("/")[-1]
                from_property_label = result["property1Label"]["value"]
                to_property_link = result["property2"]["value"]
                to_property_id = result["property2"]["value"].split("/")[-1]
                to_property_label = result["property2Label"]["value"]

                if from_property_id.startswith('P') and to_property_id.startswith('P'):
                    connection = { 'from_link': from_property_link, 'from_id': from_property_id, 'from_label': from_property_label,
                                    'to_link': to_property_link, 'to_id': to_property_id, 'to_label': to_property_label }
                    connecting_property["connections"].append(connection)
            if len(connecting_property["connections"]) > 0:
                connected_properties.append(connecting_property)

    return properties, connected_properties 

