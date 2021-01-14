from shexer.core.instances.pconsts import _S, _P, _O
from shexer.core.instances.annotators.base_annotator import BaseAnnotator

class AnnotatorTrackingInstances(BaseAnnotator):

    def __init__(self, instance_tracker):
        super().__init__(instance_tracker)

    def annotate_triple(self, a_triple):
        if self._instance_tracker.is_subclass_property(a_triple[_P]):
            self._annotate_subclass(a_triple)
        else:
            super().annotate_triple(a_triple)

    def is_relevant_triple(self, a_triple):
        if a_triple[_P] == self._subclass_property:
            return True
        else:
            return super().annotate_triple(a_triple)

    def annotation_post_parsing(self):
        for a_key_class in self._instances_dict:
            self._classes_considered_in_htree.add(a_key_class)
        iri_node = self._htree.iri_node
        for a_key_class in self._classes_considered_in_htree:
            a_class_node = self._get_appropiate_iri_node_and_add_to_htree_if_needed(a_key_class)
            if not a_class_node.has_parents():
                a_class_node.add_parent(iri_node)

    def _get_appropiate_iri_node_and_add_to_htree_if_needed(self, str_iri):
        return self._htree.get_node_of_element(str_iri) if self._htree.contains_element(str_iri) \
            else self._htree.create_node_IRI(str_iri)

    def _annotate_subclass(self, a_triple):
        str_s = str(a_triple[_S])
        str_o = str(a_triple[_O])

        subj_node = self._get_appropiate_iri_node_and_add_to_htree_if_needed(str_s)
        obj_node = self._get_appropiate_iri_node_and_add_to_htree_if_needed(str_o)
        subj_node.add_parent(obj_node)

        self._classes_considered_in_htree.add(str_s)
        self._classes_considered_in_htree.add(str_o)
