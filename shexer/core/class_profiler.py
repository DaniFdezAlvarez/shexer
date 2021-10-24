from shexer.model.IRI import IRI_ELEM_TYPE
from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.utils.target_elements import determine_original_target_nodes_if_needed
from shexer.model.property import Property
from shexer.model.IRI import IRI
from shexer.utils.uri import remove_corners
from shexer.consts import SHAPES_DEFAULT_NAMESPACE
from shexer.utils.log import log_msg

RDF_TYPE_STR = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

_POS_CLASSES = 0
_POS_FEATURES = 1

_ONE_TO_MANY = "+"

_S = 0
_P = 1
_O = 2


class ClassProfiler(object):

    def __init__(self, triples_yielder, target_classes_dict, instantiation_property_str=RDF_TYPE_STR,
                 remove_empty_shapes=True, original_target_classes=None, original_shape_map=None,
                 shapes_namespace=SHAPES_DEFAULT_NAMESPACE):
        self._triples_yielder = triples_yielder
        self._target_classes_dict = target_classes_dict  # TODO  refactor: change name once working again
        # self._instances_shape_dict = {}
        self._shapes_namespace = shapes_namespace
        self._shape_names_dict = {}  # Will be filled during execution
        self._relevant_triples = 0
        self._instantiation_property_str = self._decide_instantiation_property(instantiation_property_str)
        self._remove_empty_shapes = remove_empty_shapes
        self._original_raw_target_classes = original_target_classes
        self._classes_shape_dict = {}  # Will be filled later
        self._class_counts = {}  # Will be filled later
        self._original_target_nodes = determine_original_target_nodes_if_needed(remove_empty_shapes=remove_empty_shapes,
                                                                                original_target_classes=original_target_classes,
                                                                                original_shape_map=original_shape_map,
                                                                                shapes_namespace=shapes_namespace)


    def profile_classes(self, verbose):
        log_msg(verbose=verbose,
                msg="Starting class profiler...")
        self._init_class_counts_and_shape_dict()
        log_msg(verbose=verbose,
                msg="Instance counts completed. Annotating instance features...")
        self._adapt_instances_dict()
        self._build_shape_of_instances()
        log_msg(verbose=verbose,
                msg="Instance features annotated. Number of relevant triples computed: {}. "
                    "Building shape profiles...".format(self._relevant_triples))

        self._build_class_profile()
        log_msg(verbose=verbose,
                msg="Draft shape profiles built. Cleaning shape profiles...")
        self._clean_class_profile()
        log_msg(verbose=verbose,
                msg="Shape profiles done. Working with {} shapes.".format(len(self._classes_shape_dict)))
        return self._classes_shape_dict, self._class_counts

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


    # def _build_shape_names_dict(self):
    #     result = {}
    #     for a_class in self._target_classes_dict:
    #         name = build_shapes_name_for_class_uri(class_uri=a_class,
    #                                                shapes_namespace=self._shapes_namespace)
    #         result[a_class] = name
    #     return result


    def _init_class_counts_and_shape_dict(self):
        """
        IMPORTANT: this method should be called before adapting the instances_dict

        :return:
        """
        # self._classes_shape_dict
        for a_class in self._original_raw_target_classes:
            self._classes_shape_dict[a_class] = {}
            self._class_counts[a_class] = 0
        for an_instance, class_list in self._target_classes_dict.items():
            for a_class in class_list:
                if a_class not in self._classes_shape_dict:
                    self._classes_shape_dict[a_class] = {}
                    self._class_counts[a_class] = 0
                self._class_counts[a_class] += 1


    def _infer_3tuple_features(self, an_instance):
        result = []
        for a_prop in self._target_classes_dict[an_instance][_POS_FEATURES]:
            for a_type in self._target_classes_dict[an_instance][_POS_FEATURES][a_prop]:
                for a_valid_cardinality in self._infer_valid_cardinalities(a_prop,
                                                                           self._target_classes_dict[an_instance][_POS_FEATURES][a_prop][a_type]):
                    result.append( (a_prop, a_type, a_valid_cardinality) )
        return result


    def _infer_valid_cardinalities(self, a_property, a_cardinality):
        """
        Special teratment for self._instantiation_property_str. If thats the property, we are targetting specific URIs
        instead of the type IRI.
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
        for an_instance in self._target_classes_dict:
            feautres_3tuple = self._infer_3tuple_features(an_instance)

            for a_class in self._target_classes_dict[an_instance][_POS_CLASSES]:
                self._annotate_instance_features_for_class(a_class, feautres_3tuple)

    def _clean_class_profile(self):
        if not self._remove_empty_shapes:
            return
        shapes_to_remove = self._detect_shapes_to_remove()

        while(len(shapes_to_remove) != 0):
            self._iteration_remove_empty_shapes(shapes_to_remove)
            shapes_to_remove = self._detect_shapes_to_remove()

    def _detect_shapes_to_remove(self):
        shapes_to_remove = set()
        for a_shape_key in self._classes_shape_dict:
            if not self._is_original_target_shape(a_shape_key):
                if not self._has_it_annotated_features(a_shape_key):
                    shapes_to_remove.add(a_shape_key)
        return shapes_to_remove

    def _is_original_target_shape(self, shape_label):
        return shape_label in self._original_target_nodes

    def _has_it_annotated_features(self, shape_label):
        if shape_label not in self._classes_shape_dict:
            return False
        return len(self._classes_shape_dict[shape_label]) > 0

    def _iteration_remove_empty_shapes(self, target_shapes):
        for a_shape_label_key in self._classes_shape_dict:
            for a_prop_key in self._classes_shape_dict[a_shape_label_key]:
                # print(self._classes_shape_dict[a_shape_label_key][a_prop_key])
                for a_shape_to_remove in target_shapes:
                    if a_shape_to_remove in self._classes_shape_dict[a_shape_label_key][a_prop_key]:
                        del self._classes_shape_dict[a_shape_label_key][a_prop_key][a_shape_to_remove]
        for a_shape_to_remove in target_shapes:
            if a_shape_to_remove in self._classes_shape_dict:
                del self._classes_shape_dict[a_shape_to_remove]


    def _annotate_instance_features_for_class(self, a_class, features_3tuple):
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


    # def _is_instance_of_class(self, an_instance_str, a_class_str):
    #     if an_instance_str in self._target_classes_dict[a_class_str]:
    #         return True
    #     return False


    def _build_shape_of_instances(self):
        for a_triple in self._yield_relevant_triples():
            self._relevant_triples += 1
            self._annotate_feature_of_target_instance(a_triple)


    def _annotate_feature_of_target_instance(self, a_triple):
        str_subj = a_triple[_S].iri
        str_prop = a_triple[_P].iri
        type_obj = self._decide_type_obj(a_triple[_O], str_prop)

        obj_shapes = [] if type_obj != IRI_ELEM_TYPE else self._decide_shapes_obj(a_triple[_O].iri)

        self._introduce_needed_elements_in_shape_instances_dict(str_subj=str_subj,
                                                                str_prop=str_prop,
                                                                type_obj=type_obj,
                                                                obj_shapes=obj_shapes)
                                                                # obj=a_triple[_O])#,
                                                                #obj_shapes=obj_shapes)
        self._target_classes_dict[str_subj][_POS_FEATURES][str_prop][type_obj] += 1
        for a_shape in obj_shapes:
            self._target_classes_dict[str_subj][_POS_FEATURES][str_prop][a_shape] += 1

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
        # self._adapt_entry_dict_if_needed(str_subj)
        if str_prop not in self._target_classes_dict[str_subj][_POS_FEATURES]:
            self._target_classes_dict[str_subj][_POS_FEATURES][str_prop] = {}
        if type_obj not in self._target_classes_dict[str_subj][_POS_FEATURES][str_prop]:
            self._target_classes_dict[str_subj][_POS_FEATURES][str_prop][type_obj] = 0
        for a_shape in obj_shapes:
            if a_shape not in self._target_classes_dict[str_subj][_POS_FEATURES][str_prop]:
                self._target_classes_dict[str_subj][_POS_FEATURES][str_prop][a_shape] = 0
        # if str_subj not in self._instances_shape_dict:
        #     self._instances_shape_dict[str_subj] = {}
        # if str_prop not in self._instances_shape_dict[str_subj]:
        #     self._instances_shape_dict[str_subj][str_prop] = {}

        # if type_obj not in self._instances_shape_dict[str_subj][str_prop]:
        #     self._instances_shape_dict[str_subj][str_prop][type_obj] = 0

        # for a_shape in obj_shapes:
        #     if a_shape not in self._instances_shape_dict[str_subj][str_prop]:
        #         self._instances_shape_dict[str_subj][str_prop][a_shape] = 0

    def _adapt_instances_dict(self):
        for a_subj_key in self._target_classes_dict:
            self._target_classes_dict[a_subj_key] = (self._target_classes_dict[a_subj_key], {})

    def _adapt_entry_dict_if_needed(self, str_subj):
        if type(self._target_classes_dict[str_subj]) == list:
            self._target_classes_dict[str_subj] = (self._target_classes_dict[str_subj], {})

    def _decide_shapes_obj(self, str_obj):
        if str_obj not in self._target_classes_dict:
            return []
        return [self._get_shape_name_for_a_class(a_class) for a_class in self._target_classes_dict[str_obj][_POS_CLASSES]]
        # return self._target_classes_dict[str_obj][_POS_CLASSES]
        # result = []
        # for class_key in self._target_classes_dict:
        #     if str_obj in self._target_classes_dict[class_key]:
        #         result.append(self._shape_names_dict[class_key])
        # return result

    def _get_shape_name_for_a_class(self, a_class):
        self._assign_shape_name_if_needed(a_class)
        return self._shape_names_dict[a_class]

    def _assign_shape_name_if_needed(self, a_class):
        if a_class in self._shape_names_dict:
            return
        self._shape_names_dict[a_class] = build_shapes_name_for_class_uri(class_uri=a_class,
                                                                          shapes_namespace=self._shapes_namespace)


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
        subj = a_triple[_S]
        if not isinstance(subj, IRI):
            return False
        return subj.iri in self._target_classes_dict

        # if not isinstance(subj, BNode):
        #     return False
        # str_subj = subj.iri
        # for class_key in self._target_classes_dict:
        #     if str_subj in self._target_classes_dict[class_key]:
        #         return True
        # return False

