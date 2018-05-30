# dbpedia-shexer

Language: Python 2.7

This repository contains a software prototype to perform induction of Shapes in a RDF Graph. 

## Features
The user must provide a list of classes (URIs). The prototype will track all their instances, explore the triples in which they appear, and build with that information a profile of the each class.
The profile will be serialized into a Shape associated to the class. The results are serialized using Shape Expressions (ShEx).

### Configurations

* Free input. The prototype has been thought to be used against DBpedia, but the process of tracking the information is independent of the process of class profiling. Currently, some parsers to work with local file sin n-triples format are provided, but any other parser (or API consumer, DAO...) can be implemented to feed the class profiler.
* ShEx. Each class produce a Shape composed by a set of triple constrainst. The Shape in compilant with the current expecification of ShEx2.
* Score of thrustworthines. Every triple constraint is serialized associated to one or more comments. In the comments there is information about how many of the instances of a given class actually conform to the inferred triple constraint.
* Threshold of tolerance. All the triples found for any isntance of a given class have an effect on the in-memory class profile of that class. However, the prototype can be configured to serialize constraints with a minimun configurable score of trustworthiness.
* Literals and IRIs recognition. All kinds of literals are recognized and treated separately when inferring the constraints. In case a literal is not explicitly associated with a type in the original KG, xsd:string is used by default. When the object of a triple is an IRI, the macro IRI is used.
* Special treatment of rdf:type. The only exception to the previous feature happens when analyzing triples whose predicate is rdf:type. In those cases, if the object is an IRI, we create a triple constraint whose object is a value set containing a single element, which is the actual object of the original triple.
* Cardinality management. Some of the triples of a given instance may fit in an infinite number of constraint triples with the same predicate and object but different cardinality. For example, if a given instance has a single label specified by rdfs:label, that makes it fit with infinite triple constraints with the schema {rdfs:label xsd:string C}, where C can be any cardinality that includes the posibility of a single occurrence: {1}, + , {1,2}, {1,3}, {1,4},... Currently, our prototype just keeps rules with exact cardinality or + closure. 
* Configurable priority of cardinalities. our prototype can be configured to prioritize the less specific cardinality or the most specific one if its trustworthiness is high enough.

## Example code

The following code is handy for analyzing a) a file containing class-instance relations and b) a set of files containing the whole content of an RDF graph. It serializes a profile of each class in JSON and the inferred shapes in ShEx.

