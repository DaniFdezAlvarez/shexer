import json
from shexer.model.statement import Statement
from shexer.model.shape import Shape
from shexer.consts import RDF_TYPE, SHAPES_DEFAULT_NAMESPACE
from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.utils.target_elements import determine_original_target_nodes_if_needed
from shexer.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from shexer.model.statement import POSITIVE_CLOSURE, KLEENE_CLOSURE, OPT_CARDINALITY
from shexer.model.IRI import IRI_ELEM_TYPE
from shexer.io.shex.formater.statement_serializers.fixed_prop_choice_statement_serializer import FixedPropChoiceStatementSerializer  # TODO: REPFACTOR
from shexer.model.fixed_prop_choice_statement import FixedPropChoiceStatement


class ClassShexer(object):

    def __init__(self, class_counts_dict, class_profile_dict=None, class_profile_json_file=None,
                 remove_empty_shapes=True, original_target_classes=None, original_shape_map=None,
                 discard_useless_constraints_with_positive_closure=True, keep_less_specific=True,
                 all_compliant_mode=True, instantiation_property=RDF_TYPE, disable_or_statements=True,
                 disable_comments=False, namespaces_dict=None, tolerance_to_keep_similar_rules=0,
                 allow_opt_cardinality=True, disable_exact_cardinality=False, shapes_namespace=SHAPES_DEFAULT_NAMESPACE):
        self._class_counts_dict = class_counts_dict
        self._class_profile_dict = class_profile_dict if class_profile_dict is not None else self._load_class_profile_dict_from_file(
            class_profile_json_file)
        self._shapes_list = []
        self._remove_empty_shapes = remove_empty_shapes
        self._all_compliant_mode = all_compliant_mode
        self._disable_or_statements = disable_or_statements
        self._instantiation_property_str = str(instantiation_property)
        self._disable_comments = disable_comments
        self._discard_useless_positive_closures = discard_useless_constraints_with_positive_closure
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._keep_less_specific = keep_less_specific
        self._tolerance = tolerance_to_keep_similar_rules
        self._allow_opt_cardinality = allow_opt_cardinality
        self._disable_exact_cardinality = disable_exact_cardinality
        self._shapes_namespace = shapes_namespace

        self._original_target_nodes = determine_original_target_nodes_if_needed(remove_empty_shapes=remove_empty_shapes,
                                                                                original_target_classes=original_target_classes,
                                                                                original_shape_map=original_shape_map,
                                                                                shapes_namespace=shapes_namespace)


    def shex_classes(self, acceptance_threshold=0):
        self._build_shapes(acceptance_threshold)
        self._sort_shapes()
        self._set_valid_constraints_of_shapes()
        self._clean_empty_shapes()

        return self._shapes_list

    def _set_valid_constraints_of_shapes(self):
        for a_shape in self._shapes_list:
            self._set_valid_shape_constraints(a_shape)

    def _set_valid_shape_constraints(self, a_shape):
        valid_statements = self._select_valid_statements_of_shape(a_shape)
        if not len(valid_statements) == 0:
            if self._all_compliant_mode:
                self._modify_cardinalities_of_statements_non_compliant_with_all_instances(valid_statements)

            if self._disable_exact_cardinality:
                self._generalize_exact_cardinalities(valid_statements)

            if self._disable_comments:
                self._remove_comments_from_statements(valid_statements)
        a_shape.statements = valid_statements

    def _remove_comments_from_statements(self, valid_statements):
        for a_statement in valid_statements:
            a_statement.remove_comments()

    def _generalize_exact_cardinalities(self, statements):
        for a_statement in statements:
            if type(a_statement.cardinality) == int and a_statement.cardinality > 1:
                a_statement.cardinality = POSITIVE_CLOSURE

    def _modify_cardinalities_of_statements_non_compliant_with_all_instances(self, statements):
        for a_statement in statements:
            if a_statement.probability != 1:
                self._change_statement_cardinality_to_all_compliant(a_statement)

    def _change_statement_cardinality_to_all_compliant(self, statement):
        comment_for_current_sentence = self._turn_statement_into_comment(statement)
        statement.add_comment(comment=comment_for_current_sentence,
                              insert_first=True)
        statement.cardinality = OPT_CARDINALITY if \
            self._allow_opt_cardinality and statement.cardinality == 1 \
            else KLEENE_CLOSURE
        statement.probability = 1


    def _select_valid_statements_of_shape(self, a_shape):
        original_statements = a_shape.statements
        if len(original_statements) == 0:
            return []

        for a_statement in original_statements:  # TODO Refactor!!! This is not the place to set the serializer
            self._set_serializer_object_for_statements(a_statement)

        result = []
        for i in range(0, len(original_statements)):
            result.append(original_statements[i])

        result = self._group_constraints_with_same_prop_and_obj(result)
        result = self._group_IRI_constraints(result)
        # result = self._group_constraints_with_same_prop_but_different_obj(result)

        result.sort(reverse=True, key=lambda x: x.probability)  # Restoring order completly
        return result

    def _group_IRI_constraints(self, candidate_statements):
        result = []
        already_visited = set()
        for i in range(0, len(candidate_statements)):
            a_statement = candidate_statements[i]
            if a_statement.st_property == self._instantiation_property_str:
                result.append(a_statement)
                already_visited.add(a_statement)
            else:  # a_statement.st_property != self._instantiation_property_str:
                if a_statement not in already_visited:
                    already_visited.add(a_statement)
                    group_to_decide = [a_statement]

                    for j in range(i + 1, len(candidate_statements)):
                        if self._statements_have_same_prop(a_statement,
                                                           candidate_statements[j]):
                            group_to_decide.append(candidate_statements[j])
                            already_visited.add(candidate_statements[j])
                    if len(group_to_decide) == 1:
                        result.append(a_statement)
                    else:
                        if self._disable_or_statements:
                            for a_sentence in self._manage_group_to_decide_without_or(group_to_decide):
                                result.append(a_sentence)
                        else:
                            for a_sentence in self._manage_group_to_decide_with_or(group_to_decide):
                                result.append(a_sentence)

        return result

    def _manage_group_to_decide_without_or(self, group_to_decide):
        result = []
        to_compose = []
        for a_statement in group_to_decide:
            if self._is_an_IRI(a_statement.st_type):
                to_compose.append(a_statement)
            else:
                result.append(a_statement)
        to_compose.sort(reverse=True, key=lambda x: x.probability)
        target_sentence = self._get_IRI_statement_in_group(to_compose)
        self._remove_IRI_statements_if_useles(group_of_statements=to_compose)
        if len(to_compose) > 1:
            for a_statement in to_compose:
                if a_statement.st_type != IRI_ELEM_TYPE:
                    target_sentence.add_comment(self._turn_statement_into_comment(a_statement))
            result.append(target_sentence)
        elif len(to_compose) == 1:
            result.append(to_compose[0])
        # else  # No sentences to join

        return result

    def _get_IRI_statement_in_group(self, group_of_statements):
        for a_statement in group_of_statements:
            if a_statement.st_type == IRI_ELEM_TYPE:
                return a_statement

    def _manage_group_to_decide_with_or(self, group_to_decide):
        if not self._group_contains_IRI_statements(group_to_decide):
            for a_statement in group_to_decide:
                yield a_statement
        else:
            for a_new_statement in self._compose_statements_with_IRI_objects(group_to_decide):
                yield a_new_statement

    def _group_contains_IRI_statements(self, list_of_candidate_statements):
        for a_statement in list_of_candidate_statements:
            if a_statement.st_type == IRI_ELEM_TYPE:
                return True
        return False

    def _compose_statements_with_IRI_objects(self, list_of_candidate_statements):
        result = []
        to_compose = []
        for a_statement in list_of_candidate_statements:
            if self._is_an_IRI(a_statement.st_type):
                to_compose.append(a_statement)
            else:
                result.append(a_statement)
        to_compose.sort(reverse=True, key=lambda x: x.probability)
        target_probability = self._get_probability_of_IRI_statement_in_group(to_compose)
        self._remove_IRI_statements_if_useles(to_compose)
        if len(to_compose) > 1:  # There are som sentences to join in an OR
            composed_statement = FixedPropChoiceStatement(st_property=to_compose[0].st_property,
                                                          st_types=[a_statement.st_type for a_statement in to_compose],
                                                          cardinality=POSITIVE_CLOSURE,
                                                          probability=target_probability,
                                                          serializer_object=FixedPropChoiceStatementSerializer(
                                                              instantiation_property_str=self._instantiation_property_str,
                                                              disable_comments=self._disable_comments)
                                                          )
            for a_statement in to_compose:
                if a_statement.st_type != IRI_ELEM_TYPE:
                    composed_statement.add_comment(self._turn_statement_into_comment(a_statement))
            result.append(composed_statement)
        elif len(to_compose) == 1:  # There is just one sentence in the group to join with OR
            result.append(to_compose[0])
        # else  # No sentences to join
        return result

    def _remove_IRI_statements_if_useles(self, group_of_statements):
        # I am assuming a group of statements sorted by probability as param
        if len(group_of_statements) <= 1:
            return
        index_of_IRI_statement = -1
        for i in range(0, len(group_of_statements)):
            if group_of_statements[i].st_type == IRI_ELEM_TYPE:
                index_of_IRI_statement = i
                break
        if index_of_IRI_statement != -1:
            if group_of_statements[1].probability == group_of_statements[index_of_IRI_statement].probability:
                # the previous 'if' works, trust me, im an engineer
                del group_of_statements[index_of_IRI_statement]

    def _statements_have_similar_probability(self, more_probable_st, less_probable_st):
        if 1.0 - (less_probable_st.probability / more_probable_st.probability) <= self._tolerance:
            return True
        return False

    def _get_probability_of_IRI_statement_in_group(self, group_of_statements):
        for a_statement in group_of_statements:
            if a_statement.st_type == IRI_ELEM_TYPE:
                return a_statement.probability
        raise ValueError("There is no IRI statement within the received group")


    def _is_an_IRI(self, statement_type):
        return statement_type == IRI_ELEM_TYPE or statement_type.startswith("@")  # TODO careful here. Refactor


    def _statements_have_same_prop(self, st1, st2):
        if st1.st_property == st2.st_property:
            return True
        return False


    def _set_serializer_object_for_statements(self, statement):
        statement.serializer_object = BaseStatementSerializer(
            instantiation_property_str=self._instantiation_property_str,
            disable_comments=self._disable_comments)

    def _group_constraints_with_same_prop_and_obj(self, candidate_statements):
        result = []
        already_visited = set()
        for i in range(0, len(candidate_statements)):
            a_statement = candidate_statements[i]
            if a_statement not in already_visited:
                already_visited.add(a_statement)
                group_to_decide = [a_statement]
                for j in range(i + 1, len(candidate_statements)):
                    if self._statements_have_same_tokens(a_statement,
                                                         candidate_statements[j]):
                        group_to_decide.append(candidate_statements[j])
                        already_visited.add(candidate_statements[j])
                if len(group_to_decide) == 1:
                    result.append(a_statement)
                else:
                    result.append(self._decide_best_statement_with_cardinalities_in_comments(group_to_decide))
        return result

    def _statements_have_same_tokens(self, st1, st2):
        if st1.st_property == st2.st_property and st1.st_type == st2.st_type:
            return True
        return False

    def _decide_best_statement_with_cardinalities_in_comments(self, list_of_candidate_statements):
        if self._discard_useless_positive_closures:
            if self._is_a_group_of_statements_with_useless_positive_closure(list_of_candidate_statements):
                return self._statement_for_a_group_with_a_useless_positive_closure(list_of_candidate_statements)
        list_of_candidate_statements.sort(reverse=True, key=lambda x: x.probability)
        result = None
        if self._keep_less_specific:
            for a_statement in list_of_candidate_statements:
                if a_statement.cardinality == POSITIVE_CLOSURE:
                    result = a_statement
                    break
            if result is None:
                result = list_of_candidate_statements[0]
        else:
            for a_statement in list_of_candidate_statements:
                if a_statement.cardinality != POSITIVE_CLOSURE:
                    result = a_statement
                    break
            if result is None:
                result = list_of_candidate_statements[0]

        for a_statement in list_of_candidate_statements:
            if a_statement.cardinality != result.cardinality:
                result.add_comment(self._turn_statement_into_comment(a_statement))
        return result

    def _is_a_group_of_statements_with_useless_positive_closure(self, list_of_candidate_sentences):
        if len(list_of_candidate_sentences) != 2:
            return False
        if abs(list_of_candidate_sentences[0].probability - list_of_candidate_sentences[1].probability) > self._tolerance:
            return False
        one_if_there_is_a_single_positive_closure = -1
        for a_statement in list_of_candidate_sentences:
            if POSITIVE_CLOSURE == a_statement.cardinality:
                one_if_there_is_a_single_positive_closure *= -1
        if one_if_there_is_a_single_positive_closure == 1:
            return True
        return False

    def _turn_statement_into_comment(self, a_statement):
        return a_statement.comment_representation(namespaces_dict=self._namespaces_dict)

    def _statement_for_a_group_with_a_useless_positive_closure(self, group_of_candidate_statements):
        for a_statement in group_of_candidate_statements:
            if a_statement.cardinality != POSITIVE_CLOSURE:
                return a_statement
        raise ValueError("The received group does not contain any statement with positive closure")


    def _build_shapes(self, acceptance_threshold):
        for a_class_key in self._class_profile_dict:
            name = build_shapes_name_for_class_uri(class_uri=a_class_key,
                                                   shapes_namespace=self._shapes_namespace)
            number_of_instances = float(self._class_counts_dict[a_class_key])
            statements = []
            for a_prop_key in self._class_profile_dict[a_class_key]:
                for a_type_key in self._class_profile_dict[a_class_key][a_prop_key]:
                    for a_cardinality in self._class_profile_dict[a_class_key][a_prop_key][a_type_key]:
                        frequency = self._compute_frequency(number_of_instances,
                                                            self._class_profile_dict
                                                            [a_class_key]
                                                            [a_prop_key]
                                                            [a_type_key]
                                                            [a_cardinality])
                        if frequency >= acceptance_threshold:
                            statements.append(Statement(st_property=a_prop_key,
                                                        st_type=a_type_key,
                                                        cardinality=a_cardinality,
                                                        probability=frequency))

            a_shape = Shape(name=name,
                            class_uri=a_class_key,
                            statements=statements)
            self._shapes_list.append(a_shape)

    def _sort_shapes(self):
        for a_shape in self._shapes_list:
            a_shape.sort_statements(reverse=True,
                                    callback=self._value_to_compare_statements)

    def _clean_empty_shapes(self):

        if not self._remove_empty_shapes:
            return
        shapes_to_remove = self._detect_shapes_to_remove()

        while (len(shapes_to_remove) != 0):
            self._iteration_remove_empty_shapes(shapes_to_remove)
            shapes_to_remove = self._detect_shapes_to_remove()

    def _detect_shapes_to_remove(self):
        result = set()
        for a_shape in self._shapes_list:
            if a_shape.n_statements == 0:
                result.add(a_shape.class_uri)
        return result

    def _iteration_remove_empty_shapes(self, shape_names_to_remove):
        self._remove_shapes_without_statements(shape_names_to_remove)
        self._remove_statements_to_gone_shapes(shape_names_to_remove)

    def _remove_statements_to_gone_shapes(self, shape_names_to_remove):
        for a_shape in self._shapes_list:
            new_statements = []
            for a_statement in a_shape.statements:
                if not a_statement.st_type in shape_names_to_remove:
                    new_statements.append(a_statement)
            a_shape.statements = new_statements

    def _remove_shapes_without_statements(self, shape_names_to_remove):
        new_shape_list = []
        for a_shape in self._shapes_list:
            if not a_shape.name in shape_names_to_remove:
                new_shape_list.append(a_shape)
        self._shapes_list = new_shape_list

    def _value_to_compare_statements(self, a_statement):
        return a_statement.probability

    def _compute_frequency(self, number_of_instances, n_ocurrences_statement):
        return float(n_ocurrences_statement) / number_of_instances

    @staticmethod
    def _load_class_profile_dict_from_file(source_file):
        with open(source_file, "r") as in_stream:
            return json.load(in_stream)
