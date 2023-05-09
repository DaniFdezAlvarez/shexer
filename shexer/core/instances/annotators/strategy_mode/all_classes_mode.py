from shexer.core.instances.annotators.strategy_mode.base_strategy_mode import BaseStrategyMode
from shexer.core.instances.pconsts import _P

class AllClasesMode(BaseStrategyMode):

    def __init__(self, annotator_ref):
        super().__init__(annotator_ref)



    def is_relevant_triple(self, a_triple):
        if a_triple[_P] != self._instantiation_property:
            return False
        return True


    def annotate_triple(self, a_triple):
        if self._instance_tracker.is_an_instantiation_prop(a_triple[_P]):
            self._annotator_ref.add_instance_to_instances_dict(a_triple)
            self.annotate_class(a_triple)


