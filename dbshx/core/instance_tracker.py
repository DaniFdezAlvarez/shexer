from dbshx.model.property import Property
from dbshx.utils.uri import remove_corners
from dbshx.utils.factories.h_tree import get_basic_h_tree

_S = 0
_P = 1
_O = 2

_RDF_TYPE = Property(content="http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
_RDFS_SUBCLASS_OF = Property(content="http://www.w3.org/2000/01/rdf-schema#subClassOf")


class InstanceTracker(object):

    def __init__(self, target_classes, triples_yielder, instantiation_property=_RDF_TYPE,
                 all_classes_mode=False, subclass_property=_RDFS_SUBCLASS_OF, track_hierarchies=True):
        self._instances_dict = self._build_instances_dict(target_classes, all_classes_mode)
        self._triples_yielder = triples_yielder
        self._instantiation_property = self._decide_instantiation_property(instantiation_property)
        self._relevant_triples = 0
        self._not_relevant_triples = 0
        self._all_classes_mode = all_classes_mode
        self._subclass_property = subclass_property
        self._track_hierarchies = track_hierarchies

        self._htree = get_basic_h_tree() if track_hierarchies else None
        self._classes_considered_in_htree = set() if track_hierarchies else None

    @property
    def relevant_triples(self):
        return self._relevant_triples

    @property
    def not_relevant_triples(self):
        return self._not_relevant_triples

    @property
    def htree(self):
        return self._htree

    def track_instances(self):
        self._reset_count()
        for a_revelant_triple in self._yield_relevant_triples():
            if self._is_an_instantiation_prop(a_revelant_triple[_P]):
                self._anotate_instance(a_revelant_triple)
            elif self._track_hierarchies :  # And it is a subclass property, for sure
                self._anotate_subclass(a_revelant_triple)
        if self._track_hierarchies:
            self._anotate_direct_children_of_IRI()

        return self._instances_dict

    def _anotate_direct_children_of_IRI(self):
        for a_key_class in self._instances_dict:
            self._classes_considered_in_htree.add(a_key_class)
        iri_node = self._htree.iri_node
        for a_key_class in self._classes_considered_in_htree:
            a_class_node = self._get_appropiate_iri_node_and_add_to_htree_if_needed(a_key_class)
            if not a_class_node.has_parents():
                a_class_node.add_parent(iri_node)


    def _reset_count(self):
        self._relevant_triples = 0
        self._not_relevant_triples = 0
        self._htree = get_basic_h_tree()

    def _anotate_instance(self, a_triple):
        self._instances_dict[a_triple[_O].iri].add(a_triple[_S].iri)

    def _anotate_subclass(self, a_triple):
        str_s = str(a_triple[_S])
        str_o = str(a_triple[_O])

        subj_node = self._get_appropiate_iri_node_and_add_to_htree_if_needed(str_s)
        obj_node = self._get_appropiate_iri_node_and_add_to_htree_if_needed(str_o)
        subj_node.add_parent(obj_node)

        self._classes_considered_in_htree.add(str_s)
        self._classes_considered_in_htree.add(str_o)

    def _get_appropiate_iri_node_and_add_to_htree_if_needed(self, str_iri):
        return self._htree.get_node_of_element(str_iri) if self._htree.contains_element(str_iri) \
            else self._htree.create_node_IRI(str_iri)

    def _yield_relevant_triples(self):
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
        if self._track_hierarchies and a_triple[_P] == self._subclass_property:
            return True
        elif a_triple[_P] != self._instantiation_property:
            return False
        elif self._all_classes_mode:
            if a_triple[_O].iri not in self._instances_dict:
                self._add_new_class_to_instances_dict(a_triple[_O].iri)
                return True
        elif a_triple[_O].iri not in self._instances_dict:
            return False
        return True

    def _is_an_instantiation_prop(self, a_property):
        return a_property == self._instantiation_property

    def _is_a_subcalss_property(self, a_property):
        return a_property == self._subclass_property

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
