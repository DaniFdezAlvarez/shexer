_S = 0
_P = 1
_O = 2


from dbshx.model.property import Property

class InstanceTracker(object):

    def __init__(self, target_classes, triples_yielder):
        # self._source_file = source_file
        self._instances_dict = self._build_instances_dict(target_classes)
        self._triples_yielder = triples_yielder
        self._RDF_TYPE = Property(content="http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        self._relevant_triples = 0
        self._not_relevant_triples = 0


    @property
    def relevant_triples(self):
        return self._relevant_triples

    @property
    def not_relevant_triples(self):
        return self._not_relevant_triples

    @staticmethod
    def _build_instances_dict(target_classes):
        result = {}
        for a_class in target_classes:
            result[a_class.iri] = set()
        return result

    def _reset_count(self):
        self._relevant_triples = 0
        self._not_relevant_triples = 0


    def track_instances(self):
        self._reset_count()
        for a_triple_instance in self._yield_instantiation_triples():
            # if self._relevant_triples % 500 == 0:
            #     print "INSTANCES FOUND!", self._relevant_triples
            self._anotate_instance(a_triple_instance)
        return self._instances_dict

    def _anotate_instance(self, a_triple):
        self._instances_dict[a_triple[_O].iri].add(a_triple[_S].iri)


    def _yield_instantiation_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._is_a_relevant_triple(a_triple):
                self._relevant_triples += 1
                yield a_triple
            else:
                self._not_relevant_triples += 1

    def _is_a_relevant_triple(self, a_triple):
        """
        It returns True if the triple has rdf:type as predicate and one of the target classes as object

        :return: bool
        """
        if a_triple[_P] != self._RDF_TYPE:
            return False
        if a_triple[_O].iri not in self._instances_dict:
            return False
        return True