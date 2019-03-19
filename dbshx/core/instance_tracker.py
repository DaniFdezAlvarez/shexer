_S = 0
_P = 1
_O = 2

from dbshx.model.property import Property
from dbshx.utils.uri import remove_corners

_RDF_TYPE = Property(content="http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


class InstanceTracker(object):

    def __init__(self, target_classes, triples_yielder, instantiation_property=_RDF_TYPE, all_classes_mode=False):
        self._instances_dict = self._build_instances_dict(target_classes, all_classes_mode)
        self._triples_yielder = triples_yielder
        self._instantiation_property = self._decide_instantiation_property(instantiation_property)
        self._relevant_triples = 0
        self._not_relevant_triples = 0
        self._all_classes_mode = all_classes_mode

    @property
    def relevant_triples(self):
        return self._relevant_triples

    @property
    def not_relevant_triples(self):
        return self._not_relevant_triples

    def track_instances(self):
        self._reset_count()
        for a_triple_instance in self._yield_instantiation_triples():
            self._anotate_instance(a_triple_instance)
        return self._instances_dict

    def _reset_count(self):
        self._relevant_triples = 0
        self._not_relevant_triples = 0

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
        if a_triple[_P] != self._instantiation_property:
            return False
        if self._all_classes_mode:
            if a_triple[_O].iri not in self._instances_dict:
                self._add_new_class_to_instances_dict(a_triple[_O].iri)
                return True
        elif a_triple[_O].iri not in self._instances_dict:
            return False
        return True

    def _add_new_class_to_instances_dict(self, class_uri):

        self._instances_dict[class_uri] = set()

    @staticmethod
    def _build_instances_dict(target_classes, all_classes_mode):
        result = {}
        if all_classes_mode:
            return result  # In this case, we will add keys on the fly, while parsing the input graph.
        for a_class in target_classes:
            result[a_class.iri] = set()
        return result

    @staticmethod
    def _decide_instantiation_property(instantiation_property):
        if instantiation_property == None:
            return _RDF_TYPE
        if type(instantiation_property) == type(_RDF_TYPE):
            return instantiation_property
        if type(instantiation_property) == str:
            return Property(remove_corners(a_uri=instantiation_property,
                                           raise_error_if_no_corners=False))
        raise ValueError("Unrecognized param type to define instantiation property")
