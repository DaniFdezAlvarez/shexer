from shexer.core.profiling.strategy.abstract_strategy import AbstractStrategy
from shexer.core.profiling.consts import _S, _P, _O, _POS_FEATURES_INVERSE
from shexer.model.IRI import IRI_ELEM_TYPE

class IncludeReverseFeaturesStrategy(AbstractStrategy):


    def adapt_instances_dict(self):
        for a_subj_key in self._class_profiler._instances_dict:
            self._class_profiler._instances_dict[a_subj_key] = (self._class_profiler._instances_dict[a_subj_key], {}, {})

    def __init__(self, class_profiler):
        super().__init__(class_profiler)

    def is_a_relevant_triple(self, a_triple):
        target_elems = (a_triple[_S], a_triple[_O])
        for elem in target_elems:
            if self._is_relevant_instance(elem):
                return True
        return False


    def annotate_triple_features(self, a_triple):
        if self._is_relevant_instance(a_triple[_S]):
            self._annotate_target_subject(a_triple)
        if self._is_relevant_instance(a_triple[_O]):
            self._annotate_target_object(a_triple)


    def _annotate_target_object(self, a_triple):  # TODO: refactor here, place this in superclass and parametrize positions
        str_obj = a_triple[_S].iri
        str_prop = a_triple[_P].iri
        type_subj = self._decide_type_elem(a_triple[_S], str_prop)

        subj_shapes = [] if type_subj != IRI_ELEM_TYPE else self._decide_shapes_elem(a_triple[_S].iri)

        self._introduce_needed_elements_in_shape_instances_dict_for_obj(str_obj=str_obj,
                                                                        str_prop=str_prop,
                                                                        type_subj=type_subj,
                                                                        subj_shapes=subj_shapes)
        self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE][str_prop][type_subj] += 1
        for a_shape in subj_shapes:
            self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE][str_prop][a_shape] += 1


    def _introduce_needed_elements_in_shape_instances_dict_for_obj(self, str_obj, str_prop, type_subj, subj_shapes):
        if str_prop not in self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE]:
            self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE][str_prop] = {}
        if type_subj not in self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE][str_prop]:
            self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE][str_prop][type_subj] = 0
        for a_shape in subj_shapes:
            if a_shape not in self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE][str_prop]:
                self._class_profiler._instances_dict[str_obj][_POS_FEATURES_INVERSE][str_prop][a_shape] = 0

