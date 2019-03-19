Shapes of different celestial bodies

These shapes have been produced using all the triples in Wikidata whose sucject is an instance of planet (Q634), star (Q523), comet (Q3559), or any of their subclasses. The following configuration has been used:

* Target classes: the ones listed in the file [celestial_classes_depth_1](https://github.com/DaniFdezAlvarez/shexer/blob/develop/experiments/wikidata/celestial_bodies/celestial_classes_depth_1.tsv). 
* Aceptance threshold: 0.2
* Namespaces ignored : <http://www.wikidata.org/prop/> and <http://www.wikidata.org/prop/direct-normalized/> (most of the properties considered belong to the namespace <http://www.wikidata.org/prop/direct/>).
* inference_of_unlabelled_numeric_tipes active. This means that if there is some triple whose object is an untyped number (ex: 56 instead of "56"^^xsd:int), it will consider it a integer if does not have decimals or a float if it does.
* all_instances_are_compliant_mode active. This means that every instance of a class will conform with the shape associated to that classs using kleene closure for cardinalities when needed.
* discard_useless_constraints active. This means that if in case that there are a couple of constraints sharing property and object but with different cardinality, and one of those cardinalities is '+', with exactly the same compliance rate, the constraint with '+' will be discarded.
