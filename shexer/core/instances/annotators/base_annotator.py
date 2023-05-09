from shexer.core.instances.pconsts import _S, _P, _O
from shexer.core.instances.annotators.strategy_mode.target_classes_mode import TargetClassesMode
from shexer.core.instances.annotators.strategy_mode.all_classes_mode import AllClasesMode
from shexer.core.instances.annotators.strategy_mode.shape_qualifiers_mode import ShapeQualifiersMode
from shexer.core.instances.annotators.strategy_mode.compound_strategy_mode import CompoundStrategyMode
from shexer.core.instances.annotators.strategy_mode.instance_cap_mode import InstanceCapMode


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
        self._instances_cap = self._instance_tracker._instances_cap

        self._strategy_mode = self._get_proper_strategy()

    def is_relevant_triple(self, a_triple):
        return self._strategy_mode.is_relevant_triple(a_triple)

    def annotate_triple(self, a_triple):
        self._strategy_mode.annotate_triple(a_triple)

    def add_instance_to_instances_dict(self, a_triple):
        if a_triple[_S].iri not in self._instances_dict:
            self._instances_dict[a_triple[_S].iri] = []

    # def annotate_class(self, a_triple):
    #     self._strategy_mode.annotate_class(a_triple)

    def annotation_post_parsing(self):
        self._strategy_mode.annotation_post_parsing()


    def _get_proper_strategy(self):
        result = None
        strategies_list = []
        target_classes_flag = False
        if self._all_classes_mode:
            strategies_list.append(AllClasesMode(annotator_ref=self))
        if self._target_classes is not None and len(self._target_classes) > 0:
            strategies_list.append(TargetClassesMode(annotator_ref=self))
            target_classes_flag = True
        if self._shape_qualifiers_mode:
            strategies_list.append(
                ShapeQualifiersMode(annotator_ref=self,
                                    namespaces_for_qualifiers_props=self._namespaces_for_qualifiers_props,
                                    shapes_namespace=self._shapes_namespace))

        if len(strategies_list) == 0:
            raise ValueError("Wrong combination of params when building the instance tracker. There are not target classes")
        if len(strategies_list) == 1:
            result = strategies_list[0]
        else:
            result = CompoundStrategyMode(annotator_ref=self,
                                        list_of_strategies=strategies_list)
        return result if self._instances_cap <= 0 else \
            InstanceCapMode(annotator_ref=self,
                            internal_strategy=result,
                            instance_limit=self._instances_cap,
                            n_target_classes=-1 if not target_classes_flag or len(strategies_list) > 1
                                                   else len(self._target_classes)
                            )
