# Shexer

Try an online demo: [http://shexer.weso.es/](http://shexer.weso.es/) (and ping if you find this service down or you have any problem using it).

Language: Python 3.5
This repository contains a software prototype to perform induction of Shapes in an RDF Graph. 

## Installation

Shexer has some external dependencies listed in the files requirements.txt. You can install them all using pip:

    $ pip install -r requirements.txt

In case you are not planning to use the web service feature of this repo, you do not need to install the dependencies related to Flask.

Shexer itself can be installed using pip as well:
    
    $ pip install shexer

## Features
This library can be used to perform automatic extraction of shape expressions for a target RDF grpah. Main features:

* Several ways to provide the input data, consisting of a target graph and some target shapes. Tha graph can be provided via a raw string content, local/remote files or tracking on the fly some triples from a SPARQL endpoint. There are defined interfaces in case you want to implement some other way to provide this information. Targte shapes cna be selected by just picking some/all classes in the graph, in which case their respective instances will be used to extract the shape, or with custom node agrupations associated via shape maps.
* Valid ShEx. The produced shapes are compilant with the current expecification of ShEx2.
* Score of thrustworthines. Every triple constraint is serialized associated to one or more comments. In the comments there is information about how many of the instances of a given class actually conform to the inferred triple constraint.
* Threshold of tolerance. The constraints inferred for each shape may not be compatible with every node associated to the shapes (except constraints with Kleene closure). With this threshold you can indicate the minimun percentage of nodes that should conform with a constraint c. If c does not reach the indicated ratio, its associated information will not appear in the fina shape.
* Literals recognition. All kinds of literals are recognized and treated separately when inferring the constraints. In case a literal is not explicitly associated with a type in the original KG, xsd:string is used by default. By default, when it finds an untyped literal shexer may try to infer its type in case it is a number. Support to some other literals, such as geolocated points, will be included in future releases.
* Shapes interlinkage: sheXer is able to detect links between nodes in target shapes. If that's the case, it will create constraints relating the shapes. If it detects triples whose object is a node which dos not belong to any other shape, then it will use the macro IRI instead.
* Special treatment of rdf:type (or the specified instantiation property). The only exception to the previous feature happens when analyzing triples whose predicate is rdf:type. In those cases, if the object is an IRI, we create a triple constraint whose object is a value set containing a single element, which is the actual object of the original triple.
* Cardinality management. Some of the triples of a given instance may fit in an infinite number of constraint triples with the same predicate and object but different cardinality. For example, if a given instance has a single label specified by rdfs:label, that makes it fit with infinite triple constraints with the schema {rdfs:label xsd:string C}, where C can be any cardinality that includes the posibility of a single occurrence: {1}, + , {1,2}, {1,3}, {1,4},... Currently, our prototype just keeps rules with exact cardinality or + closure. 
* Configurable priority of cardinalities. Our prototype can be configured to prioritize the less specific cardinality or the most specific one if its trustworthiness is high enough.


## Experimental results

In the folder [experiments](https://github.com/DaniFdezAlvarez/dbpedia-shexer/tree/develop/experiments) some results of applying this tool over different graphs with different configurations are available.


## Example code

The following code is handy for analyzing a) a file containing class-instance relations and b) a set of files containing the whole content of an RDF graph. It serializes a profile of each class in JSON and the inferred shapes in ShEx.

```python
from shexer.shaper import Shaper

target_classes = [
    "http://example.org/Person",
    "http://example.org/Place"
]

output_file = "shaper_example.shex"

namespaces_dict = {"http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                   "http://example.org/": "foo"
                   }

input_nt_file = "target_graph.nt"


shaper = Shaper(target_classes=target_classes,
                graph_file_input=input_nt_file,
                namespaces_dict=namespaces_dict,  # Defaults: no prefixes
                instantiation_property="http://example.org/type")  # Default rdf:type


shaper.shex_graph(output_file=shex_target_file,
                  aceptance_threshold=0.1)

print("Done!")

```

## The Class Shaper

Most of the features provided by this software are reachable using the class Shaper. As it is shown in the previous example code, one must get an instance of Shaper with some params and execute a method to perform the schema inference.

### init
The __init__ method of Shaper includes many params, being optional most of them. Don't panic due to the high number of params. You just need to focus on three main questions:

* How are you going to provide the graph to the library? Via a raw string, a local file, a dowloadable content, an SPARQL endpoint...
* Which shapes do you want to extract? A group of target classes, every class in the graph, or custom node groupings specified with shape maps (in a string, in a file...)?
* Do you want to configure some special feature to tune the extraction process? Priority to less specific constraints, all-compliant mode...

You'll find a param in the __init__ of Shaper to provide the information in the way you want. Use it using a keyword when creating your instance of Shaper (as in the example code of this document) and just forget about the rest, Shaper will know what to do with them.

The following list describes each param of the __init__ of Shaper:

* target_classes (default None): a list containing URIs (string) of the classes whose shape must be inferred. This param should be provided iff file_target_classes is None.
* file_target_classes (default None): a path to a file containing the URIs of the classes whose shape must be inferred. The file must contain a URI per line. This param should be provided iff target_classes is None.
* input_format (default "NT"): the format of the graph which is gonna be computed. The default value is NTriples
* instances_file_input (default None): in case you have a separate file in which instantiation relations can be found, provide its path here. If you dont provide any value, the shaper will look for instances in graph_file_input or graph_list_of_file_input.
* graph_file_input (default None): a path to the file in which the target graph can be found. This param should be provided just iff graph_list_of_files_input is None
* graph_list_of_files_input (default None): in case your graph is separated in several files (all of them with the same format), provide a list of string paths to those files in this param. This param should be provided just iff graph_file_input is None
* url_graph_input (default None): Use it to provide a URL of some dowloadable RDF content available online to be used as target graph.
* list_of_url_input (default None): Use it to provide several URLs of dowloadable RDF content available online to be used as target graph.
* url_endpoint (default None): It expects the URL of an SPARQL endpoint. Use it if you want to get some relevant triples form that endpoint instead of providing a whole RDF graph. In this case, the triples will be those ones whose subject is one of the nodes used to build the sahpes (instances of a target class, result of a node selector in a shape map).
* namespaces_dict (default None): dictionary in which the keys are namespaces and the values are their expected prefixes in the outputs. This param should be provided iff namespaces_dict_file is None.
* namespaces_dict_file (default None): a path to a file containing a dictionary in json notation with the same key-value structure to define prefixes of namespaces defined for namespaces_dict. This param should be provided iff namespaces_dict is None.
* instantiation_property (default rdf:type): full URI (with no prefixes) of the property linking instances and classes (ex: P31 in Wikidata's ontology)
* namespaces_to_ignore (default None): list of namespaces of properties used in the target graph which are going to be ignored. For example, if you set namespaces_to_ignore to \[http://example.org/\], every triple whose predicate belongs to that namespace will not be computed. It just excludes properties whose name is directly in the namespace, with no other sub-namespace between the specified ones. For example, triples with http:/example.org/foo will be ignored, but triples with http://example.org/foo/foo will be computed.
* infer_numeric_types_for_untyped_literals (default False): when it is set to True, if the parser finds a triple whose object in a number untyped (something like 56 instead of "56"^^xsd:int), it will accept it and consider it an int if it has decimals or a float if it does not. If it is set to False, triples like that will raise a parsing error.
* discard_useles_constraints_with_positive_closure (default True): if it is set to True, when two constraints has been inferred with identical property and object, and one of them has '+' cardinality while the other one has a specific number of occurrences (example: {1}, {2}...), if they both have the same rate of compliance among the instances, the constraint with the '+' cardinality is discarded.
* all_instances_are_compliant_mode (default True): when set to True, every inferred constraint which is not valid for all the instances of the class associated to the shape, then the cardinality of that constraint is changed to '\*'. With this, every instance conforms to the shape associated with its class. When it is set to False, no cardinality is changed, so there may be instances that do not conform to the inferred shape.
* keep_less_specific (default True): when it is set to True, for a group of constraints with the same property and object but different cardinality, the one with less specific cardinality ('+') will be preserved, and the rest of constraints used to provide info in comments. When it is set to False, the preserved constraint will be the one with an integer as cardinality and the highest rate of conformance with the instances of the class.
* all_classes_mode (default False): when it is set to True, you do not net to provide a list of target classes. sheXer will produce a Shape for each class with at least one instance. 
* shape_map_raw (default None): Use it to provide custom groupings of nodes using a shape map as a raw string.
* shape_map_file (default None): Use it to provide to path to a local file containing custom groupings of nodes using a shape map.
* depth_for_building_subgraph (default 1): Use this param just in case you are working against a SPARQL endpoint. This integer indicates the max distance from any seed node to consider in order to track a subgraph from the endpoint. Please, remind that a high depth can cause a massive number of queries and have a huge performance cost. 
* track_classes_for_entities_at_last_depth_level (default True): Use this param just in case you are working against a SPARQL endpoint. If it set to True, it makes a step further to the distance to the seed nodes indicated in the param depth. However, it will just look for triples related to typing, not the whole neighborhood of the nodes in the last level of depth.
* shape_map_format (default const.FIXED_SHAPE_MAP): if you use a shape map, you can provide it using the Fixed syntax or the JSON syntax. In case you prefer the JSON, set this param to const.JSON.


### Method __shex\_graph__

The method __shex\_graph__  of shexer triggers all the inference process and gives back a result. It receives several parameters, being optional some of them:

* string_output (default False): when it is set to True, the method returns a string representation of the inferred shapes. It must be set to True iff output_file is None.
* output_file (default None): it specifies the path of the file in which the inferred shapes will be written. It must have a value different to None iff string_output is False.
* output_format (default "ShEx"): format in which the inferred shapes are gonna be serialized (currently, it just supports 'ShEx').
* aceptance_threshold (default 0.4): Given a certain inferred constraint __c__ for a shape __s__, the ammount of instances which conform to this constraint (ignoring constraints with '\*' cardinality) should be at least __aceptance\_threshold__. If this does not happen, then __c__ will not be included in __s__.


