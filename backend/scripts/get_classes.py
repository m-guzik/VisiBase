from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.wbi_helpers import execute_sparql_query, search_entities

from SPARQLWrapper import SPARQLWrapper, JSON

import requests



wbi_config['MEDIAWIKI_API_URL'] = 'https://wikihum.lab.dariah.pl/api.php' 
wbi_config['SPARQL_ENDPOINT_URL'] = 'https://wikihum.lab.dariah.pl/bigdata/sparql' 
wbi_config['WIKIBASE_URL'] = 'https://wikihum.lab.dariah.pl' 

wbi = WikibaseIntegrator()

pid_instance_of = search_entities(search_string="instance of", language="en", search_type="property")[0]
pid_subclass_of = search_entities(search_string="subclass of", language="en", search_type="property")[0]
pid_superclass_of = search_entities(search_string="superclass of", language="en", search_type="property")[0]


print("instance of", pid_instance_of)
print("subclass of", pid_subclass_of)
print("superclass of", pid_superclass_of)


query =  """
            SELECT DISTINCT ?instance ?instanceLabel ?relatedClass WHERE {
                ?item wdt:""" + pid_instance_of + """ ?instance .
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            """

results = execute_sparql_query(query)

classes = []
classes_ids = set()
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

    if class_id not in classes_ids:
        classes_ids.add(class_id)

for class_id in classes_ids:
    class_item = wbi.item.get(entity_id=class_id)
    class_claims = class_item.claims
    print("from", class_id)
    for claim in class_claims:
        if claim.mainsnak.datatype == "wikibase-item":
            print("property", claim.mainsnak.property_number)
            print("datavalue", claim.mainsnak.datavalue["value"])



# for class_instance in sorted(classes, key=lambda x: x['number']):
#     print(class_instance.get("id"))