
from shexer.model.IRI import IRI_ELEM_TYPE
from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.model.property import Property
from shexer.utils.uri import remove_corners

RDF_TYPE_STR = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


_ONE_TO_MANY = "+"

_S = 0
_P = 1
_O = 2


class ClassProfiler(object):

    def __init__(self, triples_yielder, target_classes_dict, instantiation_property_str=RDF_TYPE_STR):
        self._triples_yielder = triples_yielder
        self._target_classes_dict = target_classes_dict
        self._instances_shape_dict = {}
        self._classes_shape_dict = self._build_classes_shape_dict_with_just_classes()
        self._shape_names_dict = self._build_shape_names_dict()
        self._relevant_triples = 0
        self._instantiation_property_str = self._decide_instantiation_property(instantiation_property_str)




    def profile_classes(self):
        self._build_shape_of_instances()
        # print("Number of relevant triples", self._relevant_triples)
        # print("Profiler... shape of instances built!")
        self._build_class_profile()
        # print("Profiler... class profile built!")
        return self._classes_shape_dict

    def get_target_classes_dict(self):
        return self._target_classes_dict

    @staticmethod
    def _decide_instantiation_property(instantiation_property_str):
        if instantiation_property_str == None:
            return RDF_TYPE_STR
        if type(instantiation_property_str) == Property:
            return str(instantiation_property_str)
        if type(instantiation_property_str) == str:
            return remove_corners(a_uri=instantiation_property_str,
                                  raise_error_if_no_corners=False)
        raise ValueError("Unrecognized param type to define instantiation property")


    def _build_shape_names_dict(self):
        result = {}
        for a_class in self._target_classes_dict:
            name = build_shapes_name_for_class_uri(a_class)
            result[a_class] = name
        return result

    def _build_classes_shape_dict_with_just_classes(self):
        result = {}
        for a_class_key in self._target_classes_dict:
            result[a_class_key] = {}
        return result


    def _infer_3tuple_features(self, an_instance):
        result = []
        for a_prop in self._instances_shape_dict[an_instance]:
            for a_type in self._instances_shape_dict[an_instance][a_prop]:
                for a_valid_cardinality in self._infer_valid_cardinalities(a_prop,
                                                                           self._instances_shape_dict[an_instance][a_prop][a_type]):
                    result.append( (a_prop, a_type, a_valid_cardinality) )
        return result

    def _infer_valid_cardinalities(self, a_property, a_cardinality):
        """
        Special teratment for self._instantiation_property_str. If thats the property, we are targetting specific URIs instead of the type IRI.
        Cardinality will be always "1"
        :param a_property:
        :param a_cardinality:
        :return:
        """
        if a_property == self._instantiation_property_str:
            yield 1
        else:
            yield a_cardinality
            yield _ONE_TO_MANY


    def _build_class_profile(self):
        for an_instance in self._instances_shape_dict:
            feautres_3tuple = self._infer_3tuple_features(an_instance)
            for a_class in self._target_classes_dict:
                if self._is_instance_of_class(an_instance, a_class):
                    self._anotate_instance_features_for_class(a_class, feautres_3tuple)


    def _anotate_instance_features_for_class(self, a_class, features_3tuple):
        for a_feature_3tuple in features_3tuple:
            self._introduce_needed_elements_in_shape_classes_dict(a_class, a_feature_3tuple)
            # 3tuple: 0->str_prop, 1->str_type, 2->cardinality
            self._classes_shape_dict[a_class][a_feature_3tuple[0]][a_feature_3tuple[1]][a_feature_3tuple[2]] += 1

    def _introduce_needed_elements_in_shape_classes_dict(self, a_class, a_feature_3tuple):
        str_prop = a_feature_3tuple[0]
        str_type = a_feature_3tuple[1]
        cardinality = a_feature_3tuple[2]
        if str_prop not in self._classes_shape_dict[a_class]:
            self._classes_shape_dict[a_class][str_prop] = {}
        if str_type not in self._classes_shape_dict[a_class][str_prop]:
            self._classes_shape_dict[a_class][str_prop][str_type] = {}
        if cardinality not in self._classes_shape_dict[a_class][str_prop][str_type]:
            self._classes_shape_dict[a_class][str_prop][str_type][cardinality] = 0



    def _is_instance_of_class(self, an_instance_str, a_class_str):
        if an_instance_str in self._target_classes_dict[a_class_str]:
            return True
        return False


    def _build_shape_of_instances(self):
        for a_triple in self._yield_relevant_triples():
            self._relevant_triples += 1
            self._anotate_feature_of_target_instance(a_triple)


    def _anotate_feature_of_target_instance(self, a_triple):
        str_subj = a_triple[_S].iri
        str_prop = a_triple[_P].iri
        type_obj = self._decide_type_obj(a_triple[_O], str_prop)

        obj_shapes = [] if type_obj != IRI_ELEM_TYPE else self._decide_shapes_obj(a_triple[_O].iri)

        self._introduce_needed_elements_in_shape_instances_dict(str_subj=str_subj,
                                                                str_prop=str_prop,
                                                                type_obj=type_obj,
                                                                obj_shapes=obj_shapes)

        self._instances_shape_dict[str_subj][str_prop][type_obj] += 1
        for a_shape in obj_shapes:
            self._instances_shape_dict[str_subj][str_prop][a_shape] += 1

    def _decide_type_obj(self, original_object, str_prop):
        """
        Special traetment for self._instantiation_property_str property. We look for ValueSets instead of types when this property appears.

        :param original_object:
        :param str_prop:
        :return:
        """
        if str_prop != self._instantiation_property_str:
            return original_object.elem_type
        return original_object.iri


    def _introduce_needed_elements_in_shape_instances_dict(self, str_subj, str_prop, type_obj, obj_shapes):
        if str_subj not in self._instances_shape_dict:
            self._instances_shape_dict[str_subj] = {}
        if str_prop not in self._instances_shape_dict[str_subj]:
            self._instances_shape_dict[str_subj][str_prop] = {}
        if type_obj not in self._instances_shape_dict[str_subj][str_prop]:
            self._instances_shape_dict[str_subj][str_prop][type_obj] = 0
        for a_shape in obj_shapes:
            if a_shape not in self._instances_shape_dict[str_subj][str_prop]:
                self._instances_shape_dict[str_subj][str_prop][a_shape] = 0

    def _decide_shapes_obj(self, str_obj):
        result = []
        for class_key in self._target_classes_dict:
            if str_obj in self._target_classes_dict[class_key]:
                result.append(self._shape_names_dict[class_key])
        return result


    def _yield_relevant_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._is_a_relevant_triple(a_triple):
                yield a_triple

    def _is_a_relevant_triple(self, a_triple):
        """
        The subject of the triple must be an instance of at least one of the target classes.
        If it is, it returns True. False in the opposite case

        :param a_triple:
        :return: bool
        """
        return True if self._is_subject_in_target_classes(a_triple) else False

    def _is_subject_in_target_classes(self, a_triple):
        str_subj = a_triple[_S].iri
        for class_key in self._target_classes_dict:
            if str_subj in self._target_classes_dict[class_key]:
                return True
        return False
