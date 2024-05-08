from shexer.model.statement import POSITIVE_CLOSURE, KLEENE_CLOSURE, OPT_CARDINALITY
from shexer.model.IRI import IRI_ELEM_TYPE
from shexer.model.fixed_prop_choice_statement import FixedPropChoiceStatement
from shexer.io.shex.formater.statement_serializers.st_serializers_factory import StSerializerFactory
from shexer.core.shexing.strategy.minimal_iri_strategy.annotate_min_iri_strategy import AnnotateMinIriStrategy
from shexer.core.shexing.strategy.minimal_iri_strategy.ignore_min_iri_strategy import IgnoreMinIriStrategy


_DIRECT_ST_SERIALIZER = 0
_INVERSE_ST_SERIALIZER = 1


class AbstractShexingStrategy(object):

    def __init__(self, class_shexer):
        self._class_shexer = class_shexer
        self._namespaces_dict = class_shexer._namespaces_dict
        self._allow_opt_cardinality = class_shexer._allow_opt_cardinality
        self._disable_comments = self._class_shexer._disable_comments
        self._instantiation_property_str = self._class_shexer._instantiation_property_str
        self._keep_less_specific = self._class_shexer._keep_less_specific
        self._discard_useless_positive_closures = self._class_shexer._discard_useless_positive_closures
        self._tolerance = self._class_shexer._tolerance
        self._disable_or_statements = self._class_shexer._disable_or_statements
        self._all_compliant_mode = self._class_shexer._all_compliant_mode
        self._disable_exact_cardinality = self._class_shexer._disable_exact_cardinality
        self._allow_redundant_or = self._class_shexer._allow_redundant_or

        self._strategy_min_iri = AnnotateMinIriStrategy(class_shexer._class_min_iris_dict) \
            if class_shexer._detect_minimal_iri \
            else IgnoreMinIriStrategy()

        self._statement_serializer_factory = StSerializerFactory(freq_mode=class_shexer._instances_report_mode,
                                                                 decimals=class_shexer._decimals,
                                                                 instantiation_property_str=self._instantiation_property_str,
                                                                 disable_comments=self._disable_comments)


    def yield_base_shapes(self, acceptance_threshold):
        for a_shape in self._yield_base_shapes_direction_aware(acceptance_threshold=acceptance_threshold):
            self._strategy_min_iri.annotate_shape_iri(a_shape)
            yield a_shape

    def _yield_base_shapes_direction_aware(self, acceptance_threshold):
        raise NotImplementedError()

    def set_valid_shape_constraints(self, shape):
        raise NotImplementedError()

    def remove_statements_to_gone_shapes(self, shape, shape_names_to_remove):
        raise NotImplementedError()

    def _tune_list_of_valid_statements(self, valid_statements):
        """
        This method modifies the statements objects received --> no return needed
        :param valid_statements:
        :return:
        """
        if not len(valid_statements) == 0:
            valid_statements.sort(reverse=True, key=lambda x: x.probability)  # Restoring order completely
                                                                              # before changing cardinalities

            if self._all_compliant_mode:
                self._modify_cardinalities_of_statements_non_compliant_with_all_instances(valid_statements)

            if self._disable_exact_cardinality:
                self._generalize_exact_cardinalities(valid_statements)

            if self._disable_comments:
                self._remove_comments_from_statements(valid_statements)

    def _select_valid_statements_of_shape(self, original_statements):
        if len(original_statements) == 0:
            return []

        for a_statement in original_statements:  # TODO Refactor!!! This is not the place to set the serializer
            self._set_serializer_object_for_statements(a_statement)

        result = self._group_constraints_with_same_prop_and_obj(original_statements)
        result = self._group_IRI_constraints(result)

        return result

    def _compute_frequency(self, number_of_instances, n_ocurrences_statement):
        return float(n_ocurrences_statement) / number_of_instances

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

    def _turn_statement_into_comment(self, a_statement):
        return a_statement.comment_representation(namespaces_dict=self._namespaces_dict)

    def _generalize_exact_cardinalities(self, statements):
        for a_statement in statements:
            if type(a_statement.cardinality) == int and a_statement.cardinality > 1:
                a_statement.cardinality = POSITIVE_CLOSURE

    def _remove_comments_from_statements(self, valid_statements):
        for a_statement in valid_statements:
            a_statement.remove_comments()

    def _set_serializer_object_for_statements(self, statement):
        statement.serializer_object = self._statement_serializer_factory.get_base_serializer(
            is_inverse=statement.is_inverse
        )

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

    def _statement_for_a_group_with_a_useless_positive_closure(self, group_of_candidate_statements):
        for a_statement in group_of_candidate_statements:
            if a_statement.cardinality != POSITIVE_CLOSURE:
                return a_statement
        raise ValueError("The received group does not contain any statement with positive closure")

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
                    else:  # At this point, group_to_decide may contain a list of constraints with the same property and
                           # different node constraint
                        if self._disable_or_statements:
                            for a_sentence in self._manage_group_to_decide_without_or(group_to_decide):
                                result.append(a_sentence)
                        else:
                            for a_sentence in self._manage_group_to_decide_with_or(group_to_decide):
                                result.append(a_sentence)

        return result

    def _statements_have_same_prop(self, st1, st2):
        if st1.st_property == st2.st_property:
            return True
        return False

    def _manage_group_to_decide_without_or(self, group_to_decide):
        """
        At this point, the candidate sentences can sahere prop, but no obj.
        This is, every sentence in group_to_decide has an unique obj.

        if len(group_to_decide) > 2 --> IRI should be picked, everything else to comments.
        if len(group_to_decide) == 2 --> IRI if it has higher trustworthiness, the specific obj otherwhise

        :param group_to_decide:
        :return:
        """
        result = []
        to_compose = []
        for a_statement in group_to_decide:
            if self._is_an_IRI(a_statement.st_type):
                to_compose.append(a_statement)
            else:
                result.append(a_statement)
        to_compose.sort(reverse=True, key=lambda x: x.probability)
        target_sentence = self._get_IRI_statement_in_group(to_compose)  # May be None
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

    def _manage_group_to_decide_with_or(self, group_to_decide):
        if not self._group_contains_IRI_statements(group_to_decide):
            for a_statement in group_to_decide:
                yield a_statement
        else:
            for a_new_statement in self._compose_statements_with_IRI_objects(group_to_decide):
                yield a_new_statement

    def _is_an_IRI(self, statement_type):
        return statement_type == IRI_ELEM_TYPE or statement_type.startswith("@")  # TODO careful here. Refactor


    def _remove_IRI_statements_if_useles(self, group_of_statements):
        # I am assuming a group of statements sorted by probability as param
        if len(group_of_statements) <= 1:
            return False
        index_of_IRI_statement = -1
        for i in range(0, len(group_of_statements)):
            if group_of_statements[i].st_type == IRI_ELEM_TYPE:
                index_of_IRI_statement = i
                break
        if index_of_IRI_statement != -1:
            if group_of_statements[1].probability == group_of_statements[index_of_IRI_statement].probability:
                # the previous 'if' works, trust me, im an engineer
                del group_of_statements[index_of_IRI_statement]
                return True
        return False

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
        # target_probability = self._get_probability_of_IRI_statement_in_group(to_compose)
        iri_statement = self._get_IRI_statement_in_group(to_compose)
        was_removed_IRI = self._remove_IRI_statements_if_useles(to_compose)
        if not was_removed_IRI and not self._allow_redundant_or:  # The IRI macro is still there
            return [a_sentence for a_sentence in self._manage_group_to_decide_without_or(to_compose)] + result
        elif len(to_compose) > 1:  # There are some sentences to join in an OR and no IRI macro
            composed_statement = FixedPropChoiceStatement(
                st_property=to_compose[0].st_property,
                st_types=[a_statement.st_type for a_statement in to_compose],
                cardinality=POSITIVE_CLOSURE,
                probability=iri_statement.probability,
                n_occurences=iri_statement.n_occurences,
                serializer_object=self._statement_serializer_factory.get_choice_serializer(
                    is_inverse=to_compose[0].is_inverse
                ),
                is_inverse=to_compose[0].is_inverse
            )
            for a_statement in to_compose:
                if a_statement.st_type != IRI_ELEM_TYPE:
                    composed_statement.add_comment(self._turn_statement_into_comment(a_statement))
            result.append(composed_statement)
        elif len(to_compose) == 1:  # There is just one sentence in the group to join with OR
            result.append(to_compose[0])
        # else  # No sentences to join
        return result

    # def _get_probability_of_IRI_statement_in_group(self, group_of_statements):
    #     for a_statement in group_of_statements:
    #         if a_statement.st_type == IRI_ELEM_TYPE:
    #             return a_statement.probability
    #     raise ValueError("There is no IRI statement within the received group")

    def _get_IRI_statement_in_group(self, group_of_statements):
        for a_statement in group_of_statements:
            if a_statement.st_type == IRI_ELEM_TYPE:
                return a_statement
        return None

    def _statements_without_shapes_to_remove(self, original_statements, shape_names_to_remove):
        new_statements = []
        for a_statement in original_statements:
            if not a_statement.st_type in shape_names_to_remove:
                new_statements.append(a_statement)
        return new_statements
