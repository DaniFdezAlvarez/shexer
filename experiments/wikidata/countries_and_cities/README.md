Shapes of Country and Capital
These shapes have been produced using all the triples in Wikidata which sucject is an instance of country (Q6256) or capital (Q5119) using the following configuration:

* Target classes: <http://www.wikidata.org/entity/Q6256> and <http://www.wikidata.org/entity/Q5119>.
* Aceptance threshold: 0.7
* Namespaces ignored : <http://www.wikidata.org/prop/> and <http://www.wikidata.org/prop/direct-normalized/> (most of the properties considered belong to the namespace <http://www.wikidata.org/prop/direct/>).
* inference_of_unlabelled_numeric_tipes active. This means that if there is some triple whose object is an untyped number (ex: 56 instead of "56"^^xsd:int), it will consider it a integer if does not have decimals or a float if it does.
* all_instances_are_compliant_mode active. This means that every instance of a class will conform with the shape associated to that classs using kleene closure for cardinalities when needed.
* discard_useless_constraints active. This means that if in case that there are a couple of constraints sharing property and object but with different cardinality, and one of those cardinalities is '+', with exactly the same compliance rate, the constraint with '+' will be discarded.
