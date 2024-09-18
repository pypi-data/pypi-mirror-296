from typing import List
import rdflib

# brick = rdflib.Graph()
# brick.parse("https://brickschema.org/schema/1.4/Brick.ttl", format="turtle")
# print(f"Loaded {len(brick)} triples from Brick schema")

def get_all_classes(brick):
    query = """SELECT ?class WHERE {
            { ?class rdf:type owl:Class }
            UNION
            { ?class rdf:type rdfs:Class }
            }"""
    result = brick.query(query)
    classes = set(row['class'] for row in result)
    return list(classes)

def get_root_class(brick, classname: rdflib.URIRef) -> rdflib.URIRef:
    """
    Given a class, it returns the root class. One of: Brick.Point, Brick.Equipment, Brick.Location
    """
    query = """SELECT ?root_class WHERE {
        { ?class brick:aliasOf?/rdfs:subClassOf* brick:Point . BIND(brick:Point as ?root_class) }
        UNION
        { ?class brick:aliasOf?/rdfs:subClassOf* brick:Equipment . BIND(brick:Equipment as ?root_class) }
        UNION
        { ?class brick:aliasOf?/rdfs:subClassOf* brick:Location . BIND(brick:Location as ?root_class) }
    }"""
    res = list(brick.query(query, initBindings={"class": classname}))
    return res






