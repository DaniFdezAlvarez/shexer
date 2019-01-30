from dbshx.core.class_profiler import RDF_TYPE_STR
from dbshx.model.IRI import IRI_ELEM_TYPE
from dbshx.model.fixed_prop_choice_statement import FixedPropChoiceStatement
from dbshx.io.shex.formater.consts import SPACES_LEVEL_INDENTATION
from dbshx.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer  # TODO: REPFACTOR


class ShexSerializer(object):

    def __init__(self, target_file, shapes_list, aceptance_threshold=0.4, namespaces_dict=None,
                 tolerance_to_keep_similar_rules=0.15, keep_less_specific=True):
        self._target_file = target_file
        self._shapes_list = shapes_list
        self._aceptance_theshold = aceptance_threshold
        self._lines_buffer = []
        self._tolerance = tolerance_to_keep_similar_rules
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else []
        self._keep_less_specific = keep_less_specific

    def serialize_shex(self):

        self._reset_target_file()
        self._serialize_namespaces()
        for a_shape in self._shapes_list:
            self._serialize_shape(a_shape)
        self._flush()


    def _serialize_namespaces(self):
        for a_namespace in self._namespaces_dict:
            self._write_line(self._prefix_line(a_namespace), 0)
        self._serialize_empty_namespace()
        self._write_line("", 0)

    def _prefix_line(self, namespace_key):
        return "PREFIX " +  self._namespaces_dict[namespace_key] + ": <" + namespace_key + ">"

    def _serialize_empty_namespace(self):
        self._write_line("PREFIX : <http://weso.es/shapes/>")

    def _serialize_shape(self, a_shape):
        self._serialize_shape_name(a_shape)
        self._serialize_opening_of_rules()
        self._serialize_shape_rules(a_shape)
        self._serialize_closure_of_rule()
        self._serialize_shape_gap()

    def _flush(self):
        self._write_lines_buffer()

    def _write_line(self, a_line, indent_level=0):
        self._lines_buffer.append(self._indentation_spaces(indent_level) + a_line + "\n")
        if len(self._lines_buffer) >= 5000:
            self._write_lines_buffer()
            self._lines_buffer = []

    def _reset_target_file(self):
        with open(self._target_file, "w") as out_stream:
            out_stream.write("")  # Is this necessary? maybe enough to open it in 'w' mode?

    def _write_lines_buffer(self):
        with open(self._target_file, "a") as out_stream:
            for a_line in self._lines_buffer:
                out_stream.write(a_line)

    def _indentation_spaces(self, indent_level):
        result = ""
        for i in range(0, indent_level):
            result += SPACES_LEVEL_INDENTATION
        return result

    def _serialize_shape_rules(self, a_shape):
        statements = self._select_valid_statements_of_shape(a_shape)
        if len(statements) == 0:
            return

        for i in range(0, len(statements) - 1):
            for line_indent_tuple in statements[i]. \
                    get_tuples_to_serialize_line_indent_level(is_last_statement_of_shape=False,
                                                              namespaces_dict=self._namespaces_dict):
                self._write_line(a_line=line_indent_tuple[0],
                                 indent_level=line_indent_tuple[1])
        for line_indent_tuple in statements[len(statements) - 1]. \
                get_tuples_to_serialize_line_indent_level(is_last_statement_of_shape=True,
                                                          namespaces_dict=self._namespaces_dict):
            self._write_line(a_line=line_indent_tuple[0],
                             indent_level=line_indent_tuple[1])

    def _select_valid_statements_of_shape(self, a_shape):
        original_statements = [a_statement for a_statement in a_shape.yield_statements()]
        if len(original_statements) == 0 or original_statements[0].probability < self._aceptance_theshold:
            return []

        result = []
        for i in range(0, len(original_statements)):
            if original_statements[i].probability < self._aceptance_theshold:
                break  # Here I am assuming order
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
            if a_statement.st_property == RDF_TYPE_STR:
                result.append(a_statement)
                already_visited.add(a_statement)
            else:  # a_statement.st_property != RDF_TYPE_STR:
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
                    elif not self._group_contains_IRI_statements(group_to_decide):
                        for a_statement in group_to_decide:
                            result.append(a_statement)
                    else:
                        # pass
                        for a_new_statement in self._compose_statements_with_IRI_objects(group_to_decide):
                            result.append(a_new_statement)
        return result

    # def _group_constraints_with_same_prop_but_different_obj(self, candidate_statements):
    #     result = []
    #     already_visited = set()
    #     for i in range(0, len(candidate_statements)):
    #         a_statement = candidate_statements[i]
    #         if a_statement.st_property != RDF_TYPE_STR:
    #             if a_statement not in already_visited:
    #                 already_visited.add(a_statement)
    #                 group_to_decide = [a_statement]
    #                 for j in range(i + 1, len(candidate_statements)):
    #                     if self._statements_have_same_prop(a_statement,
    #                                                        candidate_statements[j]):
    #                         group_to_decide.append(candidate_statements[j])
    #                         already_visited.add(candidate_statements[j])
    #                 if len(group_to_decide) == 1:
    #                     result.append(a_statement)
    #                 else:
    #                     result.append(self._compose_statement_with_objects_in_or(group_to_decide))
    #             # pass
    #         else:
    #             result.append(a_statement)
    #     return result

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

    # def _filter_too_similar_statements(self, candidate_statements):
    #     result = []
    #     already_evaluated = set()
    #     for i in range(0, len(candidate_statements)):
    #         if candidate_statements[i] not in already_evaluated:
    #             swapping_statements = []
    #             for j in range(i+1, len(candidate_statements)):
    #                 if self._statements_have_similar_probability(candidate_statements[i],
    #                                                             candidate_statements[j]):
    #                     if self._statements_have_same_tokens(candidate_statements[i],
    #                                                     candidate_statements[j]):
    #                         swapping_statements.append(candidate_statements[j])
    #                         already_evaluated.add(candidate_statements[i])
    #                         already_evaluated.add(candidate_statements[j])
    #                 else:
    #                     break
    #             if len(swapping_statements) == 0:
    #                 result.append(candidate_statements[i])
    #             else:
    #                 result.append(self._decide_best_statement_with_cardinalities_in_comments(swapping_statements + [candidate_statements[i]]))
    #     return result

    def _group_contains_IRI_statements(self, list_of_candidate_statements):
        for a_statement in list_of_candidate_statements:
            if a_statement.st_type == IRI_ELEM_TYPE:
                return True
        return False

    def _is_an_IRI(self, statement_type):
        return statement_type == IRI_ELEM_TYPE or statement_type.startswith("@")  # TODO careful here. Refactor

    def _compose_statements_with_IRI_objects(self, list_of_candidate_statements):
        result = []
        to_compose = []
        for a_statement in list_of_candidate_statements:
            if self._is_an_IRI(a_statement.st_type):
                to_compose.append(a_statement)
            else:
                result.append(a_statement)
        to_compose.sort(reverse=True, key=lambda x: x.probability)
        target_probability = self._get_probability_or_IRI_statement_in_group(to_compose)
        self._remove_IRI_statements_if_useles(to_compose)
        composed_statement = FixedPropChoiceStatement(st_property=to_compose[0].st_property,
                                                      st_types=[a_statement.st_type for a_statement in to_compose],
                                                      cardinality="+",
                                                      probability=target_probability)

        for a_statement in to_compose:
            if a_statement.st_type != IRI_ELEM_TYPE:
                composed_statement.add_comment(self._turn_statement_into_comment(a_statement))

        result.append(composed_statement)

        return result


    def _get_probability_or_IRI_statement_in_group(self, group_of_statements):
        for a_statement in group_of_statements:
            if a_statement.st_type == IRI_ELEM_TYPE:
                return a_statement.probability
        raise ValueError("There is no IRI statement within the received group")

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
                # the previous 'if' works, trust me, im engineer
                del group_of_statements[index_of_IRI_statement]

    # def _compose_statement_with_objects_in_or(self, list_of_candidate_statements):
    #     list_of_candidate_statements.sort(reverse=True, key=lambda x: x.probability)
    #     composed_type = list_of_candidate_statements[0].st_type
    #     composed_probability = list_of_candidate_statements[0].probability
    #     for a_sentence in list_of_candidate_statements[1:]:
    #         composed_type += " OR " + a_sentence.st_type
    #         composed_probability += a_sentence.probability
    #
    #
    #
    #     result = Statement(st_property=list_of_candidate_statements[0].st_property,
    #                        st_type=composed_type,
    #                        probability=composed_probability,
    #                        cardinality="+")
    #
    #     for a_sentence in list_of_candidate_statements:
    #         for a_comment in a_sentence.comments:
    #             result.add_comment(a_comment)
    #             result.add_comment(self._turn_statement_into_comment(a_sentence))
    #
    #     return result

    def _decide_best_statement_with_cardinalities_in_comments(self, list_of_candidate_statements):
        list_of_candidate_statements.sort(reverse=True, key=lambda x: x.probability)
        result = None
        if self._keep_less_specific:
            for a_statement in list_of_candidate_statements:
                if a_statement.cardinality == "+":
                    result = a_statement
                    break
            if result is None:
                result = list_of_candidate_statements[0]
        else:
            for a_statement in list_of_candidate_statements:
                if a_statement.cardinality != "+":
                    result = a_statement
                    break
            if result is None:
                result = list_of_candidate_statements[0]

        for a_statement in list_of_candidate_statements:
            if a_statement.cardinality != result.cardinality:
                result.add_comment(self._turn_statement_into_comment(a_statement))
        return result

    def _turn_statement_into_comment(self, a_statement):
        return a_statement.probability_representation() + \
               " obj: " + BaseStatementSerializer.tune_token(a_statement.st_type,
                                                             self._namespaces_dict) +\
               ". Cardinality: " + a_statement.cardinality_representation()

    def _statements_have_similar_probability(self, more_probable_st, less_probable_st):
        if 1.0 - (less_probable_st.probability / more_probable_st.probability) <= self._tolerance:
            return True
        return False

    def _statements_have_same_prop(self, st1, st2):
        if st1.st_property == st2.st_property:
            return True
        return False

    def _statements_have_same_tokens(self, st1, st2):
        if st1.st_property == st2.st_property and st1.st_type == st2.st_type:
            return True
        return False

    def _serialize_shape_name(self, a_shape):
        self._write_line(a_shape.name.replace("@", ":"))

    def _serialize_opening_of_rules(self):
        self._write_line("{")

    def _serialize_closure_of_rule(self):
        self._write_line("}")

    def _serialize_shape_gap(self):
        self._write_line("")
        self._write_line("")
