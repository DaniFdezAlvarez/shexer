from shexer.core.instances.annotators.strategy_mode.base_strategy_mode import BaseStrategyMode


class CompoundStrategyMode(BaseStrategyMode):

    def __init__(self, annotator_ref, list_of_strategies):
        super().__init__(annotator_ref)
        self._list_of_strategies = list_of_strategies


    def is_relevant_triple(self, a_triple):
        for a_strategy in self._list_of_strategies:
            if a_strategy.is_relevant_triple(a_triple):
                return True
        return False

    def annotate_triple(self, a_triple):
        for a_strategy in self._list_of_strategies:
            a_strategy.annotate_triple(a_triple)

    def annotation_post_parsing(self):
        for a_strategy in self._list_of_strategies:
            a_strategy.annotation_post_parsing()
