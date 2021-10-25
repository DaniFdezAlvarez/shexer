
from shexer.core.profiling.strategy.abstract_strategy import AbstractStrategy
from shexer.core.profiling.consts import _S


class DirectFeaturesStrategy(AbstractStrategy):

    def __init__(self, class_profiler):
        super().__init__(class_profiler)


    def adapt_instances_dict(self):
        for a_subj_key in self._class_profiler._instances_dict:
            self._class_profiler._instances_dict[a_subj_key] = \
                (self._class_profiler._instances_dict[a_subj_key], {})

    def is_a_relevant_triple(self, a_triple):
        return self._is_relevant_instance(a_triple[_S])

    def annotate_triple_features(self, a_triple):
        self._annotate_target_subject(a_triple)

