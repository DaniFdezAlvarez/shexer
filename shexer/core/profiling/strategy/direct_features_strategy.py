
from shexer.core.profiling.strategy.abstract_strategy import AbstractStrategy
from shexer.core.profiling.consts import _S


class DirectFeaturesStrategy(AbstractStrategy):

    def __init__(self, class_profiler):
        super().__init__(class_profiler)


    def adapt_instances_dict(self):
        for a_subj_key in self._i_dict:
            self._i_dict[a_subj_key] = \
                (self._i_dict[a_subj_key], {})

    def is_a_relevant_triple(self, a_triple):
        return self._is_relevant_instance(a_triple[_S])

    def annotate_triple_features(self, a_triple):
        self._annotate_target_subject(a_triple)

    def annotate_instance_features(self, an_instance):
        self._annotate_direct_instance_features(an_instance)

    def init_annotated_targets(self):
        self._init_annotated_direct_features()

    def init_original_targets(self):
        if self._original_raw_target_classes:
            for a_class in self._original_raw_target_classes:
                self._c_shapes_dict[a_class] = {}
                self._c_counts[a_class] = 0

    def has_shape_annotated_features(self, shape_label):
        if shape_label not in self._c_shapes_dict:
            return False
        return len(self._c_shapes_dict[shape_label]) > 0


