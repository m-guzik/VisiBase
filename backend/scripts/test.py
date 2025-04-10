from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.wbi_helpers import execute_sparql_query

from SPARQLWrapper import SPARQLWrapper, JSON


def get_properties(request_id: str):
    match request_id:
        case "lexbib":
            sparql = SPARQLWrapper('https://lexbib.elex.is/query/sparql')
        case "wikibase-world":
            sparql = SPARQLWrapper('https://wikibase.world/query/sparql')
        case "wikihum":
            sparql = SPARQLWrapper('https://wikihum.lab.dariah.pl/bigdata/sparql')

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
            connecting_property = { 'id': property_id, 'link': property_link, 'label': property_label, 'connections': [] }
            connected_properties.append(connecting_property)

    for wiki_property in connected_properties:
        PROPERTY_ID = "wdt:" + wiki_property["id"]
        print(PROPERTY_ID)

        sparql.setQuery("""
                SELECT ?property1 ?property1Label ?property2 ?property2Label WHERE {
                ?property1 """ + PROPERTY_ID + """ ?property2 .
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en" }
                } """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            message = f"{result['property1']['value']} ↔ {result['property2']['value']}"
            from_property_link = result['property1']['value']
            from_property_id = result["property1"]["value"].split("/")[-1]
            from_property_label = result["property1Label"]["value"]
            to_property_link = result['property2']['value']
            to_property_id = result["property2"]["value"].split("/")[-1]
            to_property_label = result["property2Label"]["value"]

            connection = { 'from_link': from_property_link, 'from_id': from_property_id, 'from_label': from_property_label,
                            'to_link': to_property_link, 'to_id': to_property_id, 'to_label': to_property_label}
            wiki_property['connections'].append(connection)
    return properties, connected_properties 



properties_results, connected_results = get_properties('wikihum')
print(connected_results)
# properties_results, inverse_results = get_properties('lexbib')
# properties_results, inverse_results = get_properties('wikibase-world')


