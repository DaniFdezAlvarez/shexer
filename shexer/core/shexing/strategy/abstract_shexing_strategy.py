from shexer.model.statement import POSITIVE_CLOSURE, KLEENE_CLOSURE, OPT_CARDINALITY
from shexer.model.const_elem_types import NONLITERAL_ELEM_TYPE, BNODE_ELEM_TYPE, IRI_ELEM_TYPE
from shexer.model.fixed_prop_choice_statement import FixedPropChoiceStatement
from shexer.model.statement import Statement
from shexer.io.shex.formater.statement_serializers.st_serializers_factory import StSerializerFactory
from shexer.core.shexing.strategy.minimal_iri_strategy.annotate_min_iri_strategy import AnnotateMinIriStrategy
from shexer.core.shexing.strategy.minimal_iri_strategy.ignore_min_iri_strategy import IgnoreMinIriStrategy
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME


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
        result = self._group_node_constraints(result)

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

    def _group_constraints_with_same_prop_and_obj(self, candidate_statements):  # TODO REFACTORING
        result = []
        already_visited = set()
        for i in range(0, len(candidate_statements)):
            a_statement = candidate_statements[i]
            if a_statement not in already_visited:
                already_visited.add(a_statement)
                group_to_decide = MergeableConstraints()  # TODO
                for j in range(i + 1, len(candidate_statements)):
                    if self._statements_have_same_tokens(a_statement,
                                                         candidate_statements[j]):
                        group_to_decide.add_constraints(candidate_statements[j])
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

    def _decide_best_statement_with_cardinalities_in_comments(self, mergeable_constraints):  # TODO REFACTORING
        if self._discard_useless_positive_closures:
            if self._is_a_group_of_statements_with_useless_positive_closure(mergeable_constraints):
                return self._statement_for_a_group_with_a_useless_positive_closure(mergeable_constraints)
        mergeable_constraints.sort()
        result = None
        if self._keep_less_specific:
            for a_statement in mergeable_constraints.constraints():
                if a_statement.cardinality == POSITIVE_CLOSURE:
                    result = a_statement
                    break
            if result is None:
                result = mergeable_constraints.get(0)
        else:
            for a_statement in mergeable_constraints.constraints():
                if a_statement.cardinality != POSITIVE_CLOSURE:
                    result = a_statement
                    break
            if result is None:
                result = mergeable_constraints.get(0)

        for a_statement in mergeable_constraints.constraints():
            if a_statement.cardinality != result.cardinality:
                result.add_comment(self._turn_statement_into_comment(a_statement))
        return result

    def _is_a_group_of_statements_with_useless_positive_closure(self, list_of_candidate_sentences):  # todo during refactor
        if len(list_of_candidate_sentences) != 2:
            return False
        if abs(list_of_candidate_sentences.get(0).probability - list_of_candidate_sentences.get(1).probability) > self._tolerance:
            return False
        one_if_there_is_a_single_positive_closure = -1
        for a_statement in list_of_candidate_sentences:
            if POSITIVE_CLOSURE == a_statement.cardinality:
                one_if_there_is_a_single_positive_closure *= -1
        if one_if_there_is_a_single_positive_closure == 1:
            return True
        return False

    def _statement_for_a_group_with_a_useless_positive_closure(self, group_of_candidate_statements):  # TODO DURING REFACTOR
        for a_statement in group_of_candidate_statements:
            if a_statement.cardinality != POSITIVE_CLOSURE:
                return a_statement
        raise ValueError("The received group does not contain any statement with positive closure")

    def _group_node_constraints(self, candidate_statements):
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
                    group_to_decide = MergeableConstraints(a_statement)

                    result.append(self._find_and_merge_potentially_swapped_constraints(
                        mergeable_constraints=group_to_decide,
                        already_visited=already_visited,
                        all_original_statements=candidate_statements,
                        target_index_original_statements=i+1,
                    ))
        return result

    def _find_and_merge_potentially_swapped_constraints(self, mergeable_constraints,
                                                        already_visited,
                                                        all_original_statements,
                                                        target_index_original_statements):
        self._find_all_candidates_to_merge_swapped_constraints_at_node_level(
            mergeable_constraints=mergeable_constraints,
            already_visited=already_visited,
            all_original_statements=all_original_statements,
            target_index_original_statements=target_index_original_statements
        )
        return self._merge_swapped_constraints_at_node_level(  # TODO
            group_to_merge=mergeable_constraints
        )

    def _find_all_candidates_to_merge_swapped_constraints_at_node_level(self,
                                                                        mergeable_constraints,
                                                                        already_visited,
                                                                        all_original_statements,
                                                                        target_index_original_statements):
        for j in range(target_index_original_statements, len(all_original_statements)):
            if self._statements_have_same_prop_and_are_node_type(mergeable_constraints[0],  # todo check have_same_prop_behaviour
                                                                 all_original_statements[j]):
                mergeable_constraints.add(all_original_statements[j])
                already_visited.add(all_original_statements[j])
        # No need to return anything, modifying the received parameters.

    def _statements_have_same_prop_and_are_node_type(self, original_sentence,
                                                           target_sentence):
        # In this context, we can assume that the original one does not point to a literal
        if target_sentence.st_type in [IRI_ELEM_TYPE, BNODE_ELEM_TYPE]:
            return original_sentence.st_property == target_sentence.st_property
        return False

    def _merge_swapped_constraints_at_node_level(self, group_to_merge):
        if len(group_to_merge) == 1:
            return group_to_merge[0]
        group_to_merge.sort(reverse=True, key=lambda x: x.probability)
        return group_to_merge.merge_group(disable_or=self._disable_or_statements,
                                          redundant_or_allowed=self._allow_redundant_or)


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
            if self._is_a_node(a_statement.st_type):
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

    def _is_a_node(self, statement_type):
        return statement_type == IRI_ELEM_TYPE or statement_type == BNODE_ELEM_TYPE or statement_type.startswith(STARTING_CHAR_FOR_SHAPE_NAME)  # TODO careful here. Refactor


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
            if self._is_a_node(a_statement.st_type):
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




class MergeableConstraints(object):
    """
    Internal class used to handle constraints created during the voting process that should be merged into a single one.
    """
    def __init__(self, initial_constraint=None):
        self._constraints = [] if initial_constraint is None else [initial_constraint]
        self._bnode_constraint = None
        self._shape_constraints = None
        self._iri_constraint = None
        self._dominant_constraint = None
        self._disable_or = True
        self._redundant_or_enabled = False
    def add_constraints(self, statement):
        self._constraints.append(statement)
        if statement.st_type == BNODE_ELEM_TYPE:
            self._bnode_constraint = statement
        elif statement.st_type == IRI_ELEM_TYPE:
            self._iri_constraint = statement
        else:
            if self._shape_constraints is None:
                self._shape_constraints = []
            self._shape_constraints.append(statement)


    @property
    def has_bnodes(self):
        return self._bnode_constraint is not None

    @property
    def has_iri_constraint(self):
        return self._iri_constraint is not None

    @property
    def has_shape_constraints(self):
        return self._shape_constraints is not None

    def get(self, index):
        return self._constraints[index]

    def __len__(self):
        return len(self._constraints)

    def sort(self):
        self._constraints.sort(reverse=True, key=lambda x: x.probability)
        self._shape_constraints.sort(reverse=True, key=lambda x: x.probability)

    def constraints(self):
        for a_constaint in self._constraints:
            yield a_constaint

    def merge_group(self, disable_or, or_redundant_allowed):
        self.sort()
        self._disable_or = disable_or
        self._redundant_or_enabled = or_redundant_allowed
        if self.has_bnodes:
            self._bnode_merging_strategy()
        else:
            self._no_bnode_merging_strategy()
        return self._merge_content_in_single_statement()

    def _bnode_merging_strategy(self):
        if self.has_iri_constraint:  # iri + bnod = shape
            if len(self._shape_constraints) == 1 \
                    and self._iri_constraint.n_occurences + self._bnode_constraint.n_occurences \
                    == self._shape_constraints[0].n_occurences:
                self._promote_to_dominant(self._shape_constraints[0])
            else: # there are iri, bnode, and shape, not composed
                self._add_dominant(Statement(st_property=self._bnode_constraint.st_property,
                                             st_type=NONLITERAL_ELEM_TYPE,
                                             n_occurences=self._bnode_constraint.n_occurences + self._iri_constraint.n_occurences,
                                             is_inverse=self._bnode_constraint.is_inverse,
                                             probability=self._bnode_constraint.probability + self._iri_constraint.probability,
                                             cardinality=self._most_general_cardinality(self._bnode_constraint.cardinality,
                                                                                        self._iri_constraint.cardinality)

                                             ))
        elif len(self._shape_constraints) != 0 \
                and self._shape_constraints[0].n_occurences == self._bnode_constraint.n_occurences:
                # Case of at least a shape being used exactyl as many times as BNODE
            self._promote_to_dominant(self._shape_constraints[0])
        else:  # No IRI and no shape is used enough, BNODE should subsume everything.
            self._promote_to_dominant(self._bnode_constraint)

    def _no_bnode_merging_strategy(self):
        pass  # TODO

    def _merge_content_in_single_statement(self):
        pass  # TODO



    def _most_general_cardinality(self, a_card1, a_card2):
        if POSITIVE_CLOSURE in (a_card1, a_card2) or a_card1 != a_card2:
            return POSITIVE_CLOSURE
        else:
            return a_card1
    def _add_dominant(self, statement):
        self._dominant_constraint = statement

    def _promote_to_dominant(self, statement):
        self._dominant_constraint =statement
        self._constraints.remove(statement)

