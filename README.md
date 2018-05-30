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

```python
import json

from dbshx.utils.factories.iri_factory import create_IRIs_from_string_list
from dbshx.io.graph.yielder.nt_triples_yielder import NtTriplesYielder
from dbshx.core.instance_tracker import InstanceTracker
from dbshx.core.class_profiler import ClassProfiler
from dbshx.io.graph.yielder.multi_nt_triples_yielder import MultiNtTriplesYielder
from dbshx.io.shex.formater.shex_serializer import ShexSerializer
from dbshx.core.class_shexer import ClassShexer

target_classes = [
    "http://dbpedia.org/ontology/Country",
    "http://dbpedia.org/ontology/BaseballPlayer"
]


profie_classes_file = "class_profile_no_filter_TEST.json"
shex_target_file = "proto_shex_no_filter_TEST.shex"

target_file_instances = "instance_types_en.ttl"

target_base_dir_ = "./"
list_of_dbpedia_files_no_context = [
    "category_labels_en.ttl",
    "homepages_en.ttl",
    "labels_en.ttl",
    "mappingbased_literals_en.ttl",
    "page_ids_en.ttl",
    "geonames_links_en.ttl",
    "persondata_en.ttl",
    "mappingbased_objects_en.ttl",
    "article_categories_en.ttl",
    "freebase_links_en.ttl",
    "geo_coordinates_en.ttl",
    "infobox_properties_en.ttl",
    "infobox_property_definitions_en.ttl",
    "instance_types_en.ttl",
    "interlanguage_links_chapters_en.ttl",
    "skos_categories_en.ttl",
    "specific_mappingbased_properties_en.ttl",
    "uri_same_as_iri_en.ttl"
]

list_of_dbpedia_files = [target_base_dir_dbpedia + a_file_name for a_file_name in list_of_dbpedia_files_no_context]

target_model_classes = create_IRIs_from_string_list(target_classes)

yielder_for_instances = NtTriplesYielder(source_file=target_file_instances)

instance_tracker = InstanceTracker(target_classes=target_model_classes,
                                   triples_yielder=yielder_for_instances)
class_instances_target_dict = instance_tracker.track_instances()

yielder_for_profiling = MultiNtTriplesYielder(list_of_files=list_of_dbpedia_files)

class_profiler = ClassProfiler(triples_yielder=yielder_for_profiling,
                               target_classes_dict=class_instances_target_dict)
profile = class_profiler.profile_classes()

with open(profie_classes_file, "w") as out_stream:
    json.dump(profile, out_stream, indent=2)

class_count_dicts = {}

for a_class_key in class_instances_target_dict:
    class_count_dicts[a_class_key] = len(class_instances_target_dict[a_class_key])

shaper = ClassShexer(class_counts_dict=class_count_dicts,
                     class_profile_dict=profile)
                     # class_profile_json_file=profie_classes_file)
results = shaper.shex_classes()

namespaces_dict = {"http://dbpedia.org/ontology/": "dbo",
                   "http://creativecommons.org/ns#": "cc",
                   "http://www.ontologydesignpatterns.org/ont/d0.owl#": "d0",
                   "http://purl.org/dc/elements/1.1/": "dc",
                   "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#": "dul",
                   "http://www.w3.org/2002/07/owl#": "owl",
                   "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                   "http://www.w3.org/XML/1998/namespace": "xml",
                   "http://www.w3.org/2001/XMLSchema#": "xsd",
                   "http://xmlns.com/foaf/0.1/": "foaf",
                   "http://www.w3.org/ns/prov#": "prov",
                   "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
                   "http://purl.org/vocab/vann/": "vann",
                   "http://purl.org/dc/terms/": "dcterms",
                   "http://purl.org/NET/cidoc-crm/core#": "cidoccrm",
                   "http://www.w3.org/2003/01/geo/wgs84_pos#": "wgs84pos",
                   "http://www.wikidata.org/entity/": "wikidata",
                   "http://dbpedia.org/resource/": "dbr",
                   "http://dbpedia.org/property/": "dbp"
                   }
shexer = ShexSerializer(target_file=shex_target_file,
                        shapes_list=results,
                        aceptance_threshold=0.5,
                        namespaces_dict=namespaces_dict
                        )
shexer.serialize_shex()

print "Shexed!"

```

