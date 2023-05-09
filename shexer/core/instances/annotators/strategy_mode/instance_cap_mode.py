from shexer.core.instances.annotators.strategy_mode.base_strategy_mode import BaseStrategyMode
from shexer.core.instances.pconsts import _S, _P, _O
from shexer.core.instances.annotators.strategy_mode.instances_cap_exception import InstancesCapException

class InstanceCapMode(BaseStrategyMode):

    def __init__(self, annotator_ref, internal_strategy, instance_limit, n_target_classes = -1):
        super().__init__(annotator_ref)
        self._internal_strategy = internal_strategy
        self._instance_limit = instance_limit
        self._class_counts = {}
        self._n_target_classes = n_target_classes
        self._n_classes_completed = 0

        self.annotate_class = self._annotate_class_with_stop_condition if n_target_classes > 0 \
            else self._annotate_class_with_no_stop_condition


    def is_relevant_triple(self, a_triple):
        return self._check_class_counts(a_triple) and self._internal_strategy.is_relevant_triple(a_triple)

    def _check_class_counts(self, a_triple):
        """
        It returns False when it receives an instantiation triple whose class has already reached the maz number of
        instances allowed.

        :param a_triple:
        :return:
        """
        if a_triple[_P] != self._instantiation_property:
            return True
        if a_triple[_O].iri not in self._class_counts:
            return True
        if self._class_counts[a_triple[_O].iri] < self._instance_limit:
            return True
        return False


    def annotate_triple(self, a_triple):
        if self._instance_tracker.is_an_instantiation_prop(a_triple[_P]):
            self._annotator_ref.add_instance_to_instances_dict(a_triple)
            self.annotate_class(a_triple)

    def annotate_class(self, a_triple):
        raise NotImplementedError()


    def _annotate_class_with_stop_condition(self, a_triple):
        self._instances_dict[a_triple[_S].iri].append(a_triple[_O].iri)
        if a_triple[_O].iri not in self._class_counts:
            self._class_counts[a_triple[_O].iri] = 0
        self._class_counts[a_triple[_O].iri] += 1
        if self._class_counts[a_triple[_O].iri] == self._instance_limit:
            self._n_classes_completed += 1
        if self._n_classes_completed == self._n_target_classes:
            raise InstancesCapException()

    def _annotate_class_with_no_stop_condition(self, a_triple):
        self._instances_dict[a_triple[_S].iri].append(a_triple[_O].iri)
        if a_triple[_O].iri not in self._class_counts:
            self._class_counts[a_triple[_O].iri] = 0
        self._class_counts[a_triple[_O].iri] += 1