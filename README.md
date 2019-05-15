# Shexer

Try an online demo: [http://shexer.weso.es/](http://shexer.weso.es/) (and ping if you find this service down or you have any problem using it).

Language: Python 2.7

This repository contains a software prototype to perform induction of Shapes in an RDF Graph. 

## Installation

Shexer has some external dependencies listed in the files requirements.txt. You can install them all using pip:

    $ pip install -r requirements.txt

In case you are not planning to use the web service feature of this repo, you do not need to install the dependencies related to Flask.

Shexer itself can be installed using pip as well:
    
    $ pip install rdflib

## Features
The user must provide a list of classes (URIs). The prototype will track all their instances, explore the triples in which they appear, and build with that information a profile of the each class.
The profile will be serialized into a Shape associated to the class. The results are serialized using Shape Expressions (ShEx).

* Free input. The prototype has been thought to be used against DBpedia, but the process of tracking the information is independent of the process of class profiling. Currently, some parsers to work with local file sin n-triples format are provided, but any other parser (or API consumer, DAO...) can be implemented to feed the class profiler.
* ShEx. Each class produce a Shape composed by a set of triple constrainst. The Shape in compilant with the current expecification of ShEx2.
* Score of thrustworthines. Every triple constraint is serialized associated to one or more comments. In the comments there is information about how many of the instances of a given class actually conform to the inferred triple constraint.
* Threshold of tolerance. All the triples found for any isntance of a given class have an effect on the in-memory class profile of that class. However, the prototype can be configured to serialize constraints with a minimun configurable score of trustworthiness.
* Literals and IRIs recognition. All kinds of literals are recognized and treated separately when inferring the constraints. In case a literal is not explicitly associated with a type in the original KG, xsd:string is used by default. When the object of a triple is an IRI, the macro IRI is used.
* Special treatment of rdf:type. The only exception to the previous feature happens when analyzing triples whose predicate is rdf:type. In those cases, if the object is an IRI, we create a triple constraint whose object is a value set containing a single element, which is the actual object of the original triple.
* Cardinality management. Some of the triples of a given instance may fit in an infinite number of constraint triples with the same predicate and object but different cardinality. For example, if a given instance has a single label specified by rdfs:label, that makes it fit with infinite triple constraints with the schema {rdfs:label xsd:string C}, where C can be any cardinality that includes the posibility of a single occurrence: {1}, + , {1,2}, {1,3}, {1,4},... Currently, our prototype just keeps rules with exact cardinality or + closure. 
* Configurable priority of cardinalities. our prototype can be configured to prioritize the less specific cardinality or the most specific one if its trustworthiness is high enough.
* Shapes interlinkage. Shapes can point to some other shapes within its triple constraints.

## Experimental results

In the folder [experiments](https://github.com/DaniFdezAlvarez/dbpedia-shexer/tree/develop/experiments) some results of applying this tool over different graphs with different configurations are available.


## Example code

The following code is handy for analyzing a) a file containing class-instance relations and b) a set of files containing the whole content of an RDF graph. It serializes a profile of each class in JSON and the inferred shapes in ShEx.

```python
from dbshx.shaper import Shaper

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

print "Done!"

```

## Class Shaper

Most of the features provided by this software are reachable using the class Shaper. As it is shown in the previous example code, one must get an instance of Shaper with some params and execute a method to perform the schema inference.

### init
The __init__ method of Shaper includes many params, being optional most of them:

* target_classes (default None): a list containing URIs (string) of the classes whose shape must be inferred. This param should be provided iff file_target_classes is None.
* file_target_classes (default None): a path to a file containing the URIs of the classes whose shape must be inferred. The file must contain a URI per line. This param should be provided iff target_classes is None.
* input_format (default "NT"): the format of the graph which is gonna be computed. The default value is NTriples
* instances_file_input (default None): in case you have a separate file in which instantiation relations can be found, provide its path here. If you dont provide any value, the shaper will look for instances in graph_file_input or graph_list_of_file_input.
* graph_file_input (default None): a path to the file in which the target graph can be found. This param should be provided just iff graph_list_of_files_input is None
* graph_list_of_files_input (default None): in case your graph is separated in several files (all of them with the same format), provide a list of string paths to those files in this param. This param should be provided just iff graph_file_input is None
* namespaces_dict (default None): dictionary in which the keys are namespaces and the values are their expected prefixes in the outputs. This param should be provided iff namespaces_dict_file is None.
* namespaces_dict_file (default None): a path to a file containing a dictionary in json notation with the same key-value structure to define prefixes of namespaces defined for namespaces_dict. This param should be provided iff namespaces_dict is None.
* instantiation_property (default rdf:type): full URI (with no prefixes) of the property linking instances and classes (ex: P31 in Wikidata's ontology)
* namespaces_to_ignore (default None): list of namespaces of properties used in the target graph which are going to be ignored. For example, if you set namespaces_to_ignore to \[http://example.org/\], every triple whose predicate belongs to that namespace will not be computed. It just excludes properties whose name is directly in the namespace, with no other sub-namespace between the specified ones. For example, triples with http:/example.org/foo will be ignored, but triples with http://example.org/foo/foo will be computed.
* infer_numeric_types_for_untyped_literals (default False): when it is set to True, if the parser finds a triple whose object in a number untyped (something like 56 instead of "56"^^xsd:int), it will accept it and consider it an int if it has decimals or a float if it does not. If it is set to False, triples like that will raise a parsing error.
* discard_useles_constraints_with_positive_closure (default True): if it is set to True, when two constraints has been inferred with identical property and object, and one of them has '+' cardinality while the other one has a specific number of occurrences (example: {1}, {2}...), if they both have the same rate of compliance among the instances, the constraint with the '+' cardinality is discarded.
* all_instances_are_compliant_mode (default True): when set to True, every inferred constraint which is not valid for all the instances of the class associated to the shape, then the cardinality of that constraint is changed to '\*'. With this, every instance conforms to the shape associated with its class. When it is set to False, no cardinality is changed, so there may be instances that do not conform to the inferred shape.
* keep_less_specific (default True): when it is set to True, for a group of constraints with the same property and object but different cardinality, the one with less specific cardinality ('+') will be preserved, and the rest of constraints used to provide info in comments. When it is set to False, the preserved constraint will be the one with an integer as cardinality and the highest rate of conformance with the instances of the class.
* all_classes_mode (default False): when it is set to True, you do not net to provide a list of target classes. sheXer will produce a Shape for each class with at least one instance.

### Method __shex\_graph__

The method __shex\_graph__  of shexer triggers all the inference process and gives back a result. It receives several parameters, being optional some of them:

* string_output (default False): when it is set to True, the method returns a string representation of the inferred shapes. It must be set to True iff output_file is None.
* output_file (default None): it specifies the path of the file in which the inferred shapes will be written. It must have a value different to None iff string_output is False.
* output_format (default "ShEx"): format in which the inferred shapes are gonna be serialized (currently, it just supports 'ShEx').
* aceptance_threshold (default 0.4): Given a certain inferred constraint __c__ for a shape __s__, the ammount of instances which conform to this constraint (ignoring constraints with '\*' cardinality) should be at least __aceptance\_threshold__. If this does not happen, then __c__ will not be included in __s__.


