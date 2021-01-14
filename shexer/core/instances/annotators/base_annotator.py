from shexer.core.instances.pconsts import _S, _P, _O
from shexer.core.instances.annotators.strategy_mode.target_classes_mode import TargetClassesMode
from shexer.core.instances.annotators.strategy_mode.all_classes_mode import AllClasesMode
from shexer.core.instances.annotators.strategy_mode.shape_qualifiers_mode import ShapeQualifiersMode
from shexer.core.instances.annotators.strategy_mode.compound_strategy_mode import CompoundStrategyMode


class BaseAnnotator(object):

    def __init__(self, instance_tracker):
        self._instance_tracker = instance_tracker

        # Some short-path to avoid verbosity and too deep references. We'll be gentle with private stuff ;)
        self._all_classes_mode = self._instance_tracker._all_classes_mode
        self._instantiation_property = self._instance_tracker._instantiation_property
        self._subclass_property = self._instance_tracker._subclass_property
        self._instances_dict = self._instance_tracker._instances_dict
        self._classes_considered_in_htree = self._instance_tracker._classes_considered_in_htree
        self._htree = self._instance_tracker._htree
        self._shape_qualifiers_mode = self._instance_tracker._shape_qualifiers_mode
        self._namespaces_for_qualifiers_props = self._instance_tracker._namespaces_for_qualifiers_props
        self._target_classes = self._instance_tracker._target_classes
        self._shapes_namespace = self._instance_tracker._shapes_namespace

        self._strategy_mode = self._get_proper_strategy()

    def is_relevant_triple(self, a_triple):
        return self._strategy_mode.is_relevant_triple(a_triple)

        # if a_triple[_P] != self._instantiation_property:
        #     return False
        # elif self._all_classes_mode:
        #     if a_triple[_O].iri not in self._instances_dict:
        #         # The next line "shouldnt" be executed here, it fits better in annotation methods.
        #         # However, doing it here avoid to check in those methods again the conditions in which this class
        #         # should be added to the instnaceS_dict
        #         self.add_new_class_to_instances_dict(a_triple[_O].iri)
        #         return True
        # elif a_triple[_O].iri not in self._instances_dict:
        #     return False
        # return True

    def annotate_triple(self, a_triple):
        self._strategy_mode.annotate_triple(a_triple)



    def add_new_class_to_instances_dict(self, class_uri):
        if class_uri not in self._instances_dict:
            self._instances_dict[class_uri] = set()

    def annotation_post_parsing(self):
        self._strategy_mode.annotation_post_parsing()

    def annotate_instance(self, a_triple):
        self._instances_dict[a_triple[_O].iri].add(a_triple[_S].iri)

    def _get_proper_strategy(self):
        strategies_list = []
        if self._all_classes_mode:
            strategies_list.append(AllClasesMode(annotator_ref=self))
        if self._target_classes is not None and len(self._target_classes) > 0:
            strategies_list.append(TargetClassesMode(annotator_ref=self))
        if self._shape_qualifiers_mode:
            strategies_list.append(
                ShapeQualifiersMode(annotator_ref=self,
                                    namespaces_for_qualifiers_props=self._namespaces_for_qualifiers_props,
                                    shapes_namespace=self._shapes_namespace))

        if len(strategies_list) == 0:
            raise ValueError("Wrong combination of params when building the instance tracker. There are not target classes")
        if len(strategies_list) == 1:
            return strategies_list[0]
        else:
            return CompoundStrategyMode(annotator_ref=self,
                                        list_of_strategies=strategies_list)
