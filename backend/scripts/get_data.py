from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.wbi_helpers import execute_sparql_query, search_entities

import requests


def prepare_entity_info(result: dict, variable_name: str) -> tuple[dict, str]:
    entity_link =result[variable_name]["value"]
    entity_id = result[variable_name]["value"].split("/")[-1]
    entity_number = int(entity_id[1:]) 
    variable_label_name = variable_name + "Label"
    entity_label = result[variable_label_name]["value"]
    entity_info = { "link" : entity_link, 
                    "id" : entity_id,
                    "number" : entity_number,
                    "label" : entity_label }
    return entity_info, entity_id


def get_classes_connected_by_property(property_id: str, property_label: str) -> tuple[list, list]:
    classes = []
    connections = []
    classes_ids = set()

    query =  """
        SELECT DISTINCT ?firstClass ?firstClassLabel ?secondClass ?secondClassLabel WHERE {
            ?firstClass wdt:""" + property_id + """ ?secondClass .
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        } """

    results = execute_sparql_query(query)
    for result in results["results"]["bindings"]:
        first_class, first_class_id = prepare_entity_info(result, "firstClass")
        second_class, second_class_id = prepare_entity_info(result, "secondClass")

        if first_class_id not in classes_ids:
            classes.append(first_class)
            classes_ids.add(first_class_id)

        if second_class_id not in classes_ids:
            classes.append(second_class)
            classes_ids.add(second_class_id)
        
        connection_id = first_class_id + property_id + second_class_id
        connections.append({'id': connection_id,
                            'sourceId': first_class_id,
                            'targetId': second_class_id,
                            'label': property_label})

    return classes, connections


def get_classes(sparql_endpoint: str, wiki_url: str, api_endpoint: str):
    wbi_config['MEDIAWIKI_API_URL'] = api_endpoint
    wbi_config['SPARQL_ENDPOINT_URL'] = sparql_endpoint
    wbi_config['WIKIBASE_URL'] = wiki_url
    wbi_config['USER_AGENT'] = "VisiBase/0.1 (https://github.com/m-guzik/VisiBase)"

    wbi = WikibaseIntegrator()

    classes_ids = set()
    properties_ids = set()
    classes = []
    connections = []
    properties_labels = []
    pid_instance_of = search_entities(search_string="instance of", language="en", search_type="property") 
    if len(pid_instance_of) > 0:
        WDT_PREFIX = "<" + wiki_url + "/prop/direct/>"
        query =   """
                    PREFIX wdt: """ + WDT_PREFIX + """
                    PREFIX wikibase: <http://wikiba.se/ontology#>
                    PREFIX bd: <http://www.bigdata.com/rdf#>

                    SELECT DISTINCT ?instance ?instanceLabel WHERE {
                        ?item wdt:""" + pid_instance_of[0] + """ ?instance .
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                    }
                    """

        results = execute_sparql_query(query)
        for result in results["results"]["bindings"]:
            class_link =result["instance"]["value"]
            class_id = result["instance"]["value"].split("/")[-1]
            class_number = int(class_id[1:]) 
            class_label = result["instanceLabel"]["value"]
            instance_class = { "link" : class_link, 
                    "id" : class_id,
                    "number" : class_number,
                    "label" : class_label }
            classes_ids.add(class_id)
            classes.append(instance_class)

    subclass_classes = []
    subclass_connections = []
    pid_subclass_of = ''
    pid_subclass_of_search = search_entities(search_string="subclass of", language="en", search_type="property")
    if len(pid_subclass_of_search) > 0:
        pid_subclass_of = pid_subclass_of_search[0]
        properties_ids.add(pid_subclass_of)
        properties_labels.append("subclass of")
        subclass_classes, subclass_connections = get_classes_connected_by_property(pid_subclass_of_search[0], "subclass of")
    
    for connection in subclass_connections:
        connections.append(connection)

    for subclass_class in subclass_classes:
        if subclass_class.get("id") not in classes_ids:
            classes.append(subclass_class)
            classes_ids.add(subclass_class.get("id"))

    superclass_classes = []
    superclass_connections = []
    pid_superclass_of = ''
    pid_superclass_of_search = search_entities(search_string="superclass of", language="en", search_type="property")
    if len(pid_superclass_of_search) > 0:
        pid_superclass_of = pid_superclass_of_search[0]
        properties_ids.add(pid_superclass_of)
        properties_labels.append("superclass of")
        superclass_classes, superclass_connections = get_classes_connected_by_property(pid_superclass_of_search[0], "superclass of")

    for connection in superclass_connections:
        connections.append(connection)

    for superclass_class in superclass_classes:
        if superclass_class.get("id") not in classes_ids:
            classes.append(superclass_class)
            classes_ids.add(superclass_class.get("id"))

    for class_id in classes_ids:
        class_item = wbi.item.get(entity_id=class_id)
        for claim in class_item.claims:
            if claim.mainsnak.datatype == "wikibase-item":
                value_id = claim.mainsnak.datavalue["value"]["id"]
                property_id = claim.mainsnak.property_number
                if value_id in classes_ids and property_id != pid_subclass_of and property_id != pid_superclass_of:
                    property_entity = wbi.property.get(entity_id=property_id)
                    property_label = property_entity.labels.get('en').value
                    if property_id not in properties_ids:
                        properties_ids.add(property_id)
                        properties_labels.append(property_label)
                    connection_id = class_id + property_id + value_id
                    connections.append({'id': connection_id,
                                        'sourceId': class_id,
                                        'targetId': value_id,
                                        'label': property_label})
    
    edges = connections
    nodes = classes

    return classes, edges, nodes, properties_labels





def get_properties(sparql_endpoint: str, wiki_url: str) -> tuple[list, list, list, list]:
    wbi_config['SPARQL_ENDPOINT_URL'] = sparql_endpoint
    wbi_config['WIKIBASE_URL'] = wiki_url
    wbi_config['USER_AGENT'] = "VisiBase/0.1 (https://github.com/m-guzik/VisiBase)"

    
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
        "User-Agent": "VisiBase/0.1 (https://github.com/m-guzik/VisiBase)",
        "Accept": "application/sparql-results+json"
    }

    response = requests.get(sparql_endpoint, params={"query": query}, headers=headers)

    properties = []
    connected_properties = []
    edges_labels = []
    edges_ids = set()

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
                            if property_id not in edges_ids:
                                edges_ids.add(property_id)
                                edges_labels.append(property_label)

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


    return properties, connected_properties, edges, nodes, edges_labels

