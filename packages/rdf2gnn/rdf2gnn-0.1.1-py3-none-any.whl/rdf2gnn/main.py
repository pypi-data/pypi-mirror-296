import re
import random
import torch
import rdflib
from functools import reduce
from torch_geometric.data import HeteroData
# from torch_geometric.loader import LinkNeighborLoader
from itertools import chain
from collections import defaultdict
import torch.nn.functional as F
import torch_geometric.transforms as T
from torch_geometric.nn import GATConv, to_hetero
from torch_geometric import nn
from sklearn.metrics import accuracy_score
from typing import List

def hello():
    print("Hello from rdf2gnn!")
#to get the type of the node
def get_type(graph, node, fq=False):
    """
    Retrieves the RDF type of a given node in the graph.

    Parameters:
    - graph (rdflib.Graph): The RDF graph.
    - node (rdflib.term.Identifier): The node whose type is being queried.
    - fq (bool): If True, returns the fully qualified URI of the type; 
                 if False, returns the QName (namespace:local).

    Returns:
    - str: The type of the node.
    """
    v = graph.value(node, rdflib.RDF.type)
    if v is None:
        return str(type(node))
    if fq:
        return v
    else:
        return graph.qname(v)

def process_string(input_string):
    """
    Processes a string to make it suitable for use as an identifier by replacing special characters.

    Parameters:
    - input_string (str): The string to process.

    Returns:
    - str: A processed string where special characters are replaced with underscores.
    """
    if "http" in input_string:
        processed_string = re.sub(r'http://|https://|www\.|/', '', input_string)
        processed_string = re.sub(r'\W+', '_', processed_string)
    elif "<class '" in input_string:
        processed_string = input_string.split("'")[1].replace('.', '_')
    else:
        processed_string = re.sub(r'\W+', '_', input_string)
    return processed_string

#to transform the labels
def transform_labels(hetero_data, labels):
    """
    Transforms edge labels in a heterogeneous graph to numerical values based on provided labels.

    Parameters:
    - hetero_data (HeteroData): The heterogeneous graph data.
    - labels (list): A list of edge types used for labeling.

    Modifies:
    - hetero_data: Adds numerical labels to edges.
    """
    for edge_type in labels:
        hetero_data[edge_type].edge_label = torch.where(hetero_data[edge_type].edge_label == 1,
                                                         labels.index(edge_type) + 1,
                                                         hetero_data[edge_type].edge_label)

#to get the hetero object
def get_hetero_object(graph):
    """
    Converts an RDF graph into a HeteroData object suitable for use with PyTorch Geometric.

    Parameters:
    - graph (rdflib.Graph): The RDF graph to convert.

    Returns:
    - dict: A dictionary containing the converted HeteroData object and metadata.
    """
    type_dict = defaultdict(str)
    class_dict = {}
    for s, p, o in graph.triples((None, None, None)):
        s_t = get_type(graph, s)
        o_t = get_type(graph, o)
        fq_s_t = get_type(graph, s, fq=True)
        fq_o_t = get_type(graph, o, fq=True)
        type_dict[process_string(s_t)] = s_t
        type_dict[process_string(o_t)] = o_t
        type_dict[process_string(p)] = str(p)
        class_dict[process_string(s_t)] = fq_s_t
        class_dict[process_string(o_t)] = fq_o_t

    rev_type_dict = {v: k for k, v in type_dict.items()}
    
    hetero_data = HeteroData()
    unique_nodes = list(set(chain(*graph.subject_objects())))
    # dict of unique nodes and their corresponding classes
    classes = {k: rev_type_dict[get_type(graph, k)] for k in unique_nodes}
    edges = set() # set for unique edges

    class_to_entities = defaultdict(list)
    for k, v in classes.items():
        class_to_entities[v].append(k)
    #(num of nodes, num of classes)
    for k, v in class_to_entities.items():
        hetero_data[k].x = torch.rand(len(v), 150)

    class_edges = {}
    for s, p, o in graph.triples((None, None, None)):
        class_edges[(s, p, o)] = (rev_type_dict[get_type(graph, s)], rev_type_dict[str(p)], rev_type_dict[get_type(graph, o)])
        edges.add(p)

    edges = list(edges)

    class_edges_to_entities = defaultdict(list)
    for k, v in class_edges.items():
        class_edges_to_entities[v].append(k)
    # edge index = [2, num_specific_edge]num_specific_edge-> oi relation er moddhe koyta edge ase
    for k, v in class_edges_to_entities.items():
        temp_edge_index = torch.empty(2, len(v), dtype=torch.long)
        for i, (s, p, o) in enumerate(v):
            temp_edge_index[0, i] = class_to_entities[rev_type_dict[get_type(graph, s)]].index(s)
            temp_edge_index[1, i] = class_to_entities[rev_type_dict[get_type(graph, o)]].index(o)
        hetero_data[k[0], k[1], k[2]].edge_index = temp_edge_index
        # hetero_data[k[0], k[1], k[2]].edge_attr = torch.rand(len(v), len(edges)) # Additional information regarding edge. ('User' 'Plays' 'Game') for how many hours?

    original_edge_types = hetero_data.edge_types
    hetero_data = T.ToUndirected()(hetero_data)
    reverse_edge_types = [item for item in hetero_data.edge_types if 'rev' in item[1]]

    transform = T.RandomLinkSplit(
        num_val=0.1,# size of validation set
        num_test=0.1,
        disjoint_train_ratio=0.4,# size of supervised edges edge label create korar jonno
        is_undirected=True,  
        neg_sampling_ratio=0.3,# auotmatic negative edge 
        add_negative_train_samples=True,
        edge_types=original_edge_types,
        rev_edge_types=reverse_edge_types
    )
    train_data, val_data, test_data = transform(hetero_data)

    transform_labels(train_data, original_edge_types)
    transform_labels(val_data, original_edge_types)
    transform_labels(test_data, original_edge_types)

    hetero_object = {}
    hetero_object['unique_nodes'] = unique_nodes
    hetero_object['type_dict'] = type_dict
    hetero_object['rev_type_dict'] = rev_type_dict
    hetero_object['class_to_entities'] = class_to_entities
    hetero_object['class_dict'] = class_dict
    hetero_object['hetero_data'] = hetero_data
    hetero_object['original_edge_types'] = original_edge_types
    hetero_object['reverse_edge_types'] = reverse_edge_types
    hetero_object['train_data'] = train_data
    hetero_object['val_data'] = val_data
    hetero_object['test_data'] = test_data

    return hetero_object


def available_relationships_between(brick, fromc: rdflib.URIRef, to: rdflib.URIRef) -> List[rdflib.URIRef]:
    """
    Given a class, it returns the possible relationships from SHACL NodeShapes and PropertyShapes
    """

    # 1. get a parent class of 'from' which is a targetClass of a Node Shape. Get all sh:property/sh:path values on that NodeShape
    query = """SELECT ?path WHERE {
        ?from brick:aliasOf?/rdfs:subClassOf* ?fromp .
        ?to brick:aliasOf?/rdfs:subClassOf* ?top .
        { ?shape sh:targetClass ?fromp }
        UNION
        { ?fromp a sh:NodeShape . BIND(?fromp as ?shape) }
        ?shape sh:property ?prop .
        ?prop sh:path ?path .
        { ?prop sh:class ?top }
        UNION
        { ?prop sh:or/rdf:rest*/rdf:first ?top }
    }"""
    res = list(brick.query(query, initBindings={"from": fromc, "to": to}).bindings)
    paths = set([r['path'] for r in res])
    return list(paths)

def all_possible_relationships(brick) -> List[rdflib.URIRef]:
    """
    Returns all possible relationships between two classes
    """
    query = """SELECT ?path WHERE {
        {
        ?shape sh:property ?prop .
        ?prop sh:path ?path .
        }
        UNION
        {
        ?path a owl:ObjectProperty .
        }
    }"""
    res = list(brick.query(query).bindings)
    paths = set([r['path'] for r in res])
    return list(paths)


def available_relationships(brick, fromc: rdflib.URIRef) -> List[rdflib.URIRef]:
    """
    Given a class, it returns the possible relationships from the class
    """

    # 1. get a parent class of 'from' which is a targetClass of a Node Shape. Get all sh:property/sh:path values on that NodeShape
    query = """SELECT ?path WHERE {
        ?from brick:aliasOf?/rdfs:subClassOf* ?fromp .
        { ?shape sh:targetClass ?fromp }
        UNION
        { ?fromp a sh:NodeShape . BIND(?fromp as ?shape) }
        ?shape sh:property ?prop .
        ?prop sh:path ?path .
    }"""
    res = list(brick.query(query, initBindings={"from": fromc}).bindings)
    paths = set([r['path'] for r in res])
    return list(paths)

def get_all_classes(brick):
    """
    Retrieves all classes from a given RDF graph (e.g., Brick schema).

    Parameters:
    - brick (rdflib.Graph): The RDF graph containing the ontology.

    Returns:
    - List[rdflib.URIRef]: A list of all class URIs found in the graph.
    """
    query = """SELECT ?class WHERE {
            { ?class rdf:type owl:Class }
            UNION
            { ?class rdf:type rdfs:Class }
            }"""
    result = brick.query(query)
    classes = set(row['class'] for row in result)
    return list(classes)


def get_child_classes(brick: rdflib.Graph, classname: rdflib.URIRef):
    # this only gets the *immediate* child classes
    query = """SELECT ?child WHERE {
        ?child rdfs:subClassOf ?class
    }"""
    results = brick.query(query, initBindings={'class': classname})
    return set(row['child'] for row in results)

def get_child_classes_in_order(classname: rdflib.URIRef):
    order = []
    # get immediate child classes
    stack = [classname]
    while stack:
        classname = stack.pop(0) # get the top of the stack ("left" side of the list)
        order.append(classname) # add it to our order
        stack.extend(get_child_classes(classname)) # add the new children to the "right" side of the list
        
    return order


def get_parent_classes(brick: rdflib.Graph, classname: rdflib.URIRef):
    # this only gets the *immediate* parent classes
    query = """SELECT ?parent WHERE {
        ?class rdfs:subClassOf ?parent
    }"""
    results = brick.query(query, initBindings={'class': classname})
    return set(row['parent'] for row in results)

def get_parent_classes_in_order(brick: rdflib.Graph, classname: rdflib.URIRef):
    order = []
    # get immediate parent classes
    stack = [classname]
    while stack:
        classname = stack.pop(0) # get the top of the stack ("left" side of the list)
        order.append(classname) # add it to our order
        stack.extend(get_parent_classes(brick, classname)) # add the new parents to the "right" side of the list
        
    return order
