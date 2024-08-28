from shexer.core.instances.abstract_instance_tracker import  _RDF_TYPE, _RDFS_SUBCLASS_OF
from shexer.core.instances.instance_tracker import InstanceTracker
from shexer.consts import SHAPES_DEFAULT_NAMESPACE
from shexer.model.bnode import BNode
from shexer.core.instances.pconsts import _S


class EndpointInstanceTracker(InstanceTracker):

    def __init__(self, target_classes, triples_yielder, instantiation_property=_RDF_TYPE, all_classes_mode=False,
                 subclass_property=_RDFS_SUBCLASS_OF, track_hierarchies=True, shape_qualifiers_mode=False,
                 namespaces_for_qualifier_props=None, shapes_namespace=SHAPES_DEFAULT_NAMESPACE, instances_cap=-1):
        super().__init__(target_classes=target_classes,
                         triples_yielder=triples_yielder,
                         instantiation_property=instantiation_property,
                         all_classes_mode=all_classes_mode,
                         subclass_property=subclass_property,
                         track_hierarchies=track_hierarchies,
                         shape_qualifiers_mode=shape_qualifiers_mode,
                         namespaces_for_qualifier_props=namespaces_for_qualifier_props,
                         shapes_namespace=shapes_namespace,
                         instances_cap=instances_cap)

    def _yield_relevant_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._annotator.is_relevant_triple(a_triple) and self._subject_is_not_bnode(a_triple):
                self._relevant_triples += 1
                yield a_triple
            else:
                self._not_relevant_triples += 1

    def _subject_is_not_bnode(self, a_triple):
        return not isinstance(a_triple[_S], BNode)
