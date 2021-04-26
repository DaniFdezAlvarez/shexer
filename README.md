# sheXer

This library can be used to perform automatic extraction of shape expressions (ShEx) or Shapes Constraint Language (SHACL) for a target RDF grpah.

Try an online demo: [http://shexer.weso.es/](http://shexer.weso.es/) . 

Please, contact Dani Fernández at fernandezalvdaniel@uniovi.es or add an issue to this repository if you find any bug in sheXer.

Language: Python 3
This repository contains a software prototype to perform induction of Shapes in an RDF Graph. 

## Installation

Shexer has some external dependencies listed in the files requirements.txt. You can install them all using pip:

    $ pip install -r requirements.txt

In case you are not planning to use the web service feature of this repo, you do not need to install the dependencies related to Flask.

Shexer itself can be installed using pip as well:
    
    $ pip install shexer

## Features


* **Several ways to provide input data**, consisting of a target graph and some target shapes. Tha graph can be provided via raw string content, local/remote file(s), or tracking on the fly some triples from a SPARQL endpoint. There are defined interfaces in case you want to implement some other way to provide input information. 
* **Several ways to select your target shapes**. You may want to generate shapes for each class in the graph or maybe just for some of them. You may want to generate a shape for some custom node agrupations. Or maybe you are extracting some shapes from a big grpah and you just want to explore the neighborhood of some seed nodes.  For custom node aggrupations sheXer supports ShEx's shape maps syntax, and it provides configuration params to target different classes or graph depths. 
* **Valid ShEx and SHACL**. The produced shapes are compilant with the current specification of ShEx2 and SHACL.
* **Threshold of tolerance**. The constraints inferred for each shape may not be compatible with every node associated to the shapes. With this threshold you can indicate the minimun percentage of nodes that should conform with a constraint c. If c does not reach the indicated ratio, its associated information will not appear in the final shape.
* **Informative comments** (just for ShEx, by now). Each constraint inferred is associated to one or more comments. Those comments include different types of information, such as the ratio of nodes that actually conform with a given constraint. You can keep this informative comments or exclude them from the results.
* **Sorted constraints** (just for ShEx, by now). For a given constraint, sheXer keeps the ratio of nodes that conform with it. This is used as a score of trustworthiness. The constraints in a shape are sorted w.r.t. this score.
* **Literals recognition**. All kinds of typed literals are recognized and treated separately when inferring the constraints. In case a literal is not explicitly associated with a type in the original KG, xsd:string is used by default. By default, when sheXer finds an untyped literal it tries to infer its type when it is a number. Support to some other untyped literals, such as geolocated points, may be included in future releases.
* **Shapes interlinkage**: sheXer is able to detect links between shapes when there is a link between two nodes and those nodes are used to extract some shape. When it detects triples linking a node that does not belong to any other shape, then it uses the macro IRI instead.
* **Special treatment of rdf:type** (or the specified instantiation property). When the predicate of a triple is rdf:type, sheXer creates a constraint whose object is a value set containing a single element. This is the actual object of the original triple.
* **Cardinality management**. Some of the triples of a given instance may fit in an infinite number of constraint triples with the same predicate and object but different cardinality. For example, if a given instance has a single label specified by rdfs:label, that makes it fit with infinite triple constraints with the schema {rdfs:label xsd:string C}, where C can be any cardinality that includes the posibility of a single occurrence: {1}, + , {1,2}, {1,3}, {1,4},... Currently, sheXer admints exact cardinalities ({2}, {3}..), kleene closure (\*), positive closure (+), and optional cardinality (?).
* **Configurable priority of cardinalities**. sheXer can be configured to prioritize the less specific cardinality or the most specific one if its trustworthiness score is high enough.
* **All compliant mode**: You can produce shapes that conform with every instance using to extract them. This is done by using cadinalities \* or ? for every constraint extracted that does not conform with EVERY instance. You may prefer to avoid these cardinalities and keep constraints that may not conform with every instance, but include the most frequent features of the instances. Both settings are available in sheXer.
* **Manage of empty shapes**. You may get some shapes with no constraints, either because there where no isntances to explore or because the extracted features were not as common as requested with the threshold of tolerance. You can configure sheXer to automatically erase those shapes and every mention to them from the results. 
* **Adaptation to Wikidata model**. sheXer includes configuration params to handle Wikidata's data model regarding qualifiers, so you can automatically extract the schema of qualifier nodes too.

## Experimental results

In the folder [experiments](https://github.com/DaniFdezAlvarez/dbpedia-shexer/tree/develop/experiments), you can see some results of applying this tool over different graphs with different configurations.


## Example code

The following code is takes the graph in _raw\_graph_ and extracts shapes for instances of the classes <http://example.org/Person> and <http://example.org/Gender>. The input file format in n-triples and the results are serialized in ShExC to the file shaper_example.shex.

```python
from shexer.shaper import Shaper
from shexer.consts import NT, SHEXC, SHACL_TURTLE

target_classes = [
    "http://example.org/Person",
    "http://example.org/Gender"
]

namespaces_dict = {"http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                   "http://example.org/": "ex",
                   "http://weso.es/shapes/": "",
                   "http://www.w3.org/2001/XMLSchema#": "xml"
                   }

raw_graph = """
<http://example.org/sarah> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Person> .
<http://example.org/sarah> <http://example.org/age> "30"^^<http://www.w3.org/2001/XMLSchema#int> .
<http://example.org/sarah> <http://example.org/name> "Sarah" .
<http://example.org/sarah> <http://example.org/gender> <http://example.org/Female> .
<http://example.org/sarah> <http://example.org/occupation> <http://example.org/Doctor> .
<http://example.org/sarah> <http://example.org/brother> <http://example.org/Jim> .

<http://example.org/jim> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Person> .
<http://example.org/jim> <http://example.org/age> "28"^^<http://www.w3.org/2001/XMLSchema#int> .
<http://example.org/jim> <http://example.org/name> "Jimbo".
<http://example.org/jim> <http://example.org/surname> "Mendes".
<http://example.org/jim> <http://example.org/gender> <http://example.org/Male> .

<http://example.org/Male> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Gender> .
<http://example.org/Male> <http://www.w3.org/2000/01/rdf-schema#label> "Male" .
<http://example.org/Female> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Gender> .
<http://example.org/Female> <http://www.w3.org/2000/01/rdf-schema#label> "Female" .
<http://example.org/Other> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Gender> .
<http://example.org/Other> <http://www.w3.org/2000/01/rdf-schema#label> "Other gender" .
"""



input_nt_file = "target_graph.nt"

shaper = Shaper(target_classes=target_classes,
                raw_graph=raw_graph,
                input_format=NT,
                namespaces_dict=namespaces_dict,  # Default: no prefixes
                instantiation_property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type")  # Default rdf:type

output_file = "shaper_example.shex"

shaper.shex_graph(output_file=output_file,
                  acceptance_threshold=0.1)

print("Done!")

```

By default, sheXer generates ShExC. If you want to produce SHACL, indicate it as a param in the shex_graph method as follows:

```python
# Use the same imports and param definition of the previous example code

output_file = "shaper_example.ttl"

shaper.shex_graph(output_file=output_file,
                  acceptance_threshold=0.1,
                  output_format=SHACL_TURTLE)

print("Done!")

```


## The Class Shaper

Most of the features provided by this software are reachable using the class Shaper. As it is shown in the previous example code, one must get an instance of Shaper with some params and execute a method to perform the schema extraction.

### init
The __init__ method of Shaper includes many params, being optional most of them. Don't panic due to the high number of params. You just need to focus on three main questions:

* How are you going to provide the graph to the library? Via a raw string, a local file, a downloadable content, an SPARQL endpoint...
* Which shapes do you want to extract? A group of target classes, every class in the graph, or custom node groupings specified with shape maps (in a string, in a file...)?
* Do you want to configure some special feature to tune the extraction process? Priority to less specific constraints, all-compliant mode, disbale comments...

You'll find a param in the __init__ of Shaper to provide the information in the way you want. Use it using a keyword when creating your instance of Shaper (as in the example code of this document) and just forget about the rest. Shaper has a default value for them all.

The following list describes each param of the __init__ of Shaper:

#### Params to define target shapes:
You must indicate al least one way to identify target instances and the shapes that should be generated. Some of this params are compatible, some others are not. For example, sheXer do not allow to indicate target classes and to activate all-classes mode, as it is contradictory. However, you can provide a shape map to make custom node aggrupations and use all_classes mode too, so you obtain shapes for those groupings and for each class.

* target_classes (default None): a list containing URIs (string) of the classes whose shape must be extracted. 
* file_target_classes (default None): a path to a file containing the URIs of the classes whose shape must be extracted. 
* all_classes_mode (default False): when it is set to True, you do not net to provide a list of target classes. sheXer will produce a shape for each class with at least one instance. 
* shape_map_raw (default None): use it to provide custom groupings of nodes using a shape map as a raw string.
* shape_map_file (default None): use it to provide a path to a local file containing custom groupings of nodes using a shape map.

#### Params to provide the input
You must provide at least an input: a file, a string, an endpoint, a remote graph... you may also want to tune some other aspects, such as the format of the input or namespace-prefix pairs to be used.


* instances_file_input (default None): in case you have a separate file in which instantiation relations can be found, provide its path here. If you dont provide any value, the shaper will look for instances in the graph used as input.
* graph_file_input (default None): a path to the file in which the target graph can be found.
* graph_list_of_files_input (default None): in case your graph is separated in several files (all of them with the same format), provide a list of string paths to those files here.
* raw_graph (default None): a simple raw string containing the target graph.
* url_graph_input (default None): use it to provide a URL of some downloadable RDF content available online to be used as target graph.
* list_of_url_input (default None): use it to provide several URLs of downloadable RDF content available online to be used as target graph.
* url_endpoint (default None): it expects the URL of an SPARQL endpoint. Use it if you want to get some relevant triples form that endpoint instead of providing a whole RDF graph. In this case, the triples will be those ones whose subject is one of the nodes used to build the shapes (instances of a target class, result of a node selector in a shape map).
* depth_for_building_subgraph (default 1): use this param just in case you are working against a SPARQL endpoint. This integer indicates the max distance from any seed node to consider in order to track a subgraph from the endpoint. Please, remind that a high depth can cause a massive number of queries and have a high performance cost. 
* track_classes_for_entities_at_last_depth_level (default True): use this param just in case you are working against a SPARQL endpoint. If it set to True, it makes a step further to the distance to the seed nodes indicated in the param depth. However, it will just look for triples related to typing, not the whole neighborhood of the nodes in the last level of depth.
* limit_instances_remote (default -1). Use this param if you are working against an endpoint using the param target_classes. If it is set to a positive number, sheXer will just get limit_instances_remote instances for each class from the endpoint (by adding LIMIT at the end of the sparql query). This is useful when working with big sources with tons on instances, causing too many or too heavy SPARQL queries to retrieve  all the content. 
* namespaces_dict (default None): dictionary in which the keys are namespaces and the values are their expected prefixes in the outputs. 
* input_format (default "NT"): the format of the graph which is going to be computed. The default value is const.NT. IMPORTANT: currently, sheXer does not guess input format, so ensure you specify the format here in case you are not providing n-triples content. In case you provide a combined input (several files, several URLs...) they all should have the same format. If you work against an endpoit, then this param do not have any effect.

#### Params to tune the shexing process

All this parameters have a default value so you do not need to use any of them. But you can modify the schema extraction in many different ways.

* instantiation_property (default rdf:type): full URI (no prefixes) of the property linking instances and classes (ex: P31 in Wikidata's ontology)
* namespaces_to_ignore (default None): list of namespaces of properties used in the target graph which are going to be ignored. For example, if you set namespaces_to_ignore to \[http://example.org/\], every triple whose predicate belongs to that namespace will not be computed. It just excludes properties whose name is a direct child of the namespace. For example, triples with <http:/example.org/foo> will be ignored, but triples with <http://example.org/anotherLevel/foo> will be computed.
* infer_numeric_types_for_untyped_literals (default False): when it is set to True, if the parser finds a triple whose object in a number untyped (something like 56 instead of "56"^^xsd:int), it will accept it and consider it an int if it has decimals or a float if it does not. If it is set to False, triples like that will raise a parsing error.
* discard_useles_constraints_with_positive_closure (default True): if it is set to True, when two constraints have been extracted with identical property and object, and one of them has '+' cardinality while the other one has a specific number of occurrences (example: {1}, {2}...), if they both have the same rate of compliance among the instances, the constraint with the '+' cardinality is discarded.
* all_instances_are_compliant_mode (default True): when set to True, every inferred constraint which is not valid for all the instances of the class associated to the shape, then the cardinality of that constraint is changed to '\*' or '?'. With this, every instance conforms to the shape associated with its class. When it is set to False, no cardinality is changed, so there may be instances that do not conform to the inferred shape.
* keep_less_specific (default True): when it is set to True, for a group of constraints with the same property and object but different cardinality, the one with less specific cardinality ('+') will be preserved, and the rest of constraints used to provide info in comments. When it is set to False, the preserved constraint will be the one with an integer as cardinality and the highest rate of conformance with the instances of the class.
* disable_or_statements (default True): when set to False, sheXer tries to infer constraints with the operator oneOf (|) in case there are constraints with the same property but different object. By default, sheXer groups those constraint in a isngle one having the less general object possible. For instance, when the objects are different shapes, it merges the constraints a single one whose object is IRI.
* allow_opt_cardinality (default True). When all-compliant mode is active, if there is a constraint which does not conform with every isntance but its maximun cardinality for any instance is {1}, it uses the optional cardinality (?). When set to False, it uses Kleene closure instead.
* disable_opt_cardinality (dafault False). When set to True, it prevents any constraint to have a higher cardinality higher than one, even if every instance has that cardinality. For example, a constraint such as *ex:alias xsd:string {3}* will be changed to *ex:alias xsd:string +*.
* shape_qualifiers_mode (default False). When set to True, it assumes a data model similar to Wikidata's one, where entity nodes are linked with qualifiers (BNodes) instead of the actual object meant by the triple. It is used to produce legible shapes for those special BNodes.
* namespaces_for_qualifier_props (default None). Provide here a list of namespace in which the indirect properties used to link an entity with a qualifier node can be found. A reasonable configuration for Wikidata is namespaces_for_qualifier_props = \["http://www.wikidata.org/prop/"\] .


#### Params to tune some features of the output
Again, all these params have a default value and you don't need to worry about them unless you want to tune the output.

* remove_empty_shapes (default True). When set to True, the result does not contain any empty shape nor any mention to it. If a shape A has a constraint pointing to a shape B and B is empty, then the constraint is modified and the macro IRI is used instead of B.
* disable_comments (dafault False). When set to True, the results do not contain comments.
* shapes_namespace (default: http://weso.es/shapes/). This property allows you to change the namespace in which the shape labels are created in case you do not want to use the default one. The prefix of this namespace will be the empty prefix unless the empty prefix is already being used by other namespace. In that case, sheXer looks for other preferred prefixes, or will generate a random one if any of the default ones is available. 
* wikidata_annotation (default: False). This param can be used when the output will contain Wikidata IDs. Using the library [wLighter](https://github.com/DaniFdezAlvarez/wLighter), the ourput is annotated with comments that associate a given every Wikidata ID with its English label. 


### Method __shex\_graph__

The method __shex\_graph__  of shexer triggers all the inference process and gives back a result. It receives several parameters, being optional some of them:

* string_output (default False): when it is set to True, the method returns a string representation of the inferred shapes. It must be set to True iff output_file is None.
* output_file (default None): it specifies the path of the file in which the inferred shapes will be written. It must have a value different to None iff string_output is False.
* output_format (default "ShExC"): format in which the inferred shapes will be serialized. The values currently supported are const.SHEXC and const.SHACLE_TURTLE
* aceptance_threshold (default 0): Given a certain inferred constraint __c__ for a shape __s__, the ammount of instances which conform to this constraint (ignoring constraints with '\*' cardinality) should be at least __aceptance\_threshold__. If this does not happen, then __c__ will not be included in __s__.


