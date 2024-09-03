from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker, _RDF_TYPE, _RDFS_SUBCLASS_OF
from shexer.consts import SHAPES_DEFAULT_NAMESPACE
from shexer.utils.log import log_msg
from shexer.core.instances.annotators.strategy_mode.instances_cap_exception import InstancesCapException
from shexer.utils.factories.h_tree import get_basic_h_tree
from shexer.core.instances.annotators.annotator_func import get_proper_annotator




class InstanceTracker(AbstractInstanceTracker):

    def __init__(self, target_classes, triples_yielder, instantiation_property=_RDF_TYPE,
                 all_classes_mode=False, subclass_property=_RDFS_SUBCLASS_OF, track_hierarchies=True,
                 shape_qualifiers_mode=False, namespaces_for_qualifier_props=None,
                 shapes_namespace=SHAPES_DEFAULT_NAMESPACE, instances_cap=-1):
        self._target_classes = target_classes
        self._all_classes_mode = all_classes_mode
        self._instances_dict = self._build_instances_dict()
        self._triples_yielder = triples_yielder
        self._instantiation_property = self._decide_instantiation_property(instantiation_property)
        self._relevant_triples = 0
        self._not_relevant_triples = 0
        self._subclass_property = subclass_property
        self._track_hierarchies = track_hierarchies
        self._shape_qualifiers_mode = shape_qualifiers_mode
        self._namespaces_for_qualifiers_props = [] if namespaces_for_qualifier_props is None else namespaces_for_qualifier_props
        self._shapes_namespace = shapes_namespace
        self._instances_cap = instances_cap

        self._htree = get_basic_h_tree() if track_hierarchies else None
        self._classes_considered_in_htree = set() if track_hierarchies else None

        self._annotator = get_proper_annotator(track_hierarchies=track_hierarchies,
                                               instance_tracker_ref=self)

    def _specific_disambiguator_prefix(self):
        return "class_"

    @property
    def relevant_triples(self):
        return self._relevant_triples

    @property
    def not_relevant_triples(self):
        return self._not_relevant_triples

    @property
    def htree(self):
        return self._htree

    def track_instances(self, verbose=False):
        log_msg(verbose=verbose,
                msg="Starting instance tracker...")
        self._reset_count()
        try:
            for a_revelant_triple in self._yield_relevant_triples():
                self._annotator.annotate_triple(a_revelant_triple)
        except InstancesCapException:
            pass  # It's OK, we just don't need to explore more
        self._annotator.annotation_post_parsing()
        log_msg(verbose=verbose,
                msg="Instance tracker finished. {} instances located".format(len(self._instances_dict)))
        return self._instances_dict

    def _yield_relevant_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._annotator.is_relevant_triple(a_triple):
                self._relevant_triples += 1
                yield a_triple
            else:
                self._not_relevant_triples += 1


    def is_an_instantiation_prop(self, a_property):
        return a_property == self._instantiation_property

    def is_a_subclass_property(self, a_property):
        return a_property == self._subclass_property






