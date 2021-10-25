from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.core.profiling.consts import _POS_CLASSES, _S, _P, _O, _POS_FEATURES_DIRECT
from shexer.model.IRI import IRI_ELEM_TYPE, IRI

class AbstractStrategy(object):

    def __init__(self, class_profiler):
        self._class_profiler = class_profiler

    def adapt_instances_dict(self):
        raise NotImplementedError()

    def is_a_relevant_triple(self, a_triple):
        raise NotImplementedError()

    def annotate_triple_features(self, a_triple):
        raise NotImplementedError()

    def _is_relevant_instance(self, an_instance):
        return isinstance(an_instance, IRI) and an_instance.iri in self._class_profiler._instances_dict

    def _decide_type_elem(self, original_elem, str_prop):
        """
        Special traetment for self._instantiation_property_str property. We look for ValueSets instead of types when this property appears.

        :param original_elem:
        :param str_prop:
        :return:
        """
        if str_prop != self._class_profiler._instantiation_property_str:
            return original_elem.elem_type
        return original_elem.iri

    def _decide_shapes_elem(self, str_elem):
        if str_elem not in self._class_profiler._instances_dict:
            return []
        return [self._get_shape_name_for_a_class(a_class)
                for a_class in self._class_profiler._instances_dict[str_elem][_POS_CLASSES]]

    def _get_shape_name_for_a_class(self, a_class):
        self._assign_shape_name_if_needed(a_class)
        return self._class_profiler._shape_names_dict[a_class]

    def _assign_shape_name_if_needed(self, a_class):
        if a_class in self._class_profiler._shape_names_dict:
            return
        self._class_profiler._shape_names_dict[a_class] = \
            build_shapes_name_for_class_uri(class_uri=a_class,
                                            shapes_namespace=self._class_profiler._shapes_namespace)

    def _annotate_target_subject(self, a_triple):
        str_subj = a_triple[_S].iri
        str_prop = a_triple[_P].iri
        type_obj = self._decide_type_elem(a_triple[_O], str_prop)

        obj_shapes = [] if type_obj != IRI_ELEM_TYPE else self._decide_shapes_elem(a_triple[_O].iri)

        self._introduce_needed_elements_in_shape_instances_dict_for_subj(str_subj=str_subj,
                                                                         str_prop=str_prop,
                                                                         type_obj=type_obj,
                                                                         obj_shapes=obj_shapes)
        self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT][str_prop][type_obj] += 1
        for a_shape in obj_shapes:
            self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT][str_prop][a_shape] += 1


    def _introduce_needed_elements_in_shape_instances_dict_for_subj(self, str_subj, str_prop, type_obj, obj_shapes):
        if str_prop not in self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT]:
            self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT][str_prop] = {}
        if type_obj not in self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT][str_prop]:
            self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT][str_prop][type_obj] = 0
        for a_shape in obj_shapes:
            if a_shape not in self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT][str_prop]:
                self._class_profiler._instances_dict[str_subj][_POS_FEATURES_DIRECT][str_prop][a_shape] = 0