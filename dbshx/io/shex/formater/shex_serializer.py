
from dbshx.core.class_profiler import RDF_TYPE_STR
from dbshx.model.statement import Statement

_SPACES_GAP_FOR_FREQUENCY = "          "
_SPACES_GAP_BETWEEN_TOKENS = "  "
_TARGET_LINE_LENGHT = 60
_SPACES_LEVEL_INDENTATION = "   "
_COMMENT_INI = "# "
# _WHOTES_POR_STANDALONE_COMMENT = "                                        "  # 40


class ShexSerializer(object):

    def __init__(self, target_file, shapes_list, aceptance_threshold=0.4, namespaces_dict=None, tolerance_to_keep_similar_rules=0.15, keep_less_specific=True):
        self._target_file = target_file
        self._shapes_list = shapes_list
        self._aceptance_theshold = aceptance_threshold
        self._lines_buffer = []
        self._tolerance = tolerance_to_keep_similar_rules
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else []
        self._keep_less_specific = keep_less_specific


    def serialize_shex(self):

        self._reset_target_file()
        for a_shape in self._shapes_list:
            self._serialize_shape(a_shape)
        self._flush()


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
            result += _SPACES_LEVEL_INDENTATION
        return result


    def _serialize_shape_rules(self, a_shape):
        statements = self._select_valid_statements_of_shape(a_shape)
        if len(statements) == 0:
            return

        for i in range(0, len(statements) - 1 ):
            self._serialize_statement(a_statement=statements[i],
                                      is_last_statement_of_shape=False)
        self._serialize_statement(a_statement=statements[len(statements) - 1],
                                  is_last_statement_of_shape=True)

    def _select_valid_statements_of_shape(self, a_shape):
        original_statements = [a_statement for a_statement in a_shape.yield_statements()]
        result = []
        if len(original_statements) == 0 or original_statements[0].probability < self._aceptance_theshold:
            return []

        for i in range(0, len(original_statements)):
            if original_statements[i].probability < self._aceptance_theshold:

                break
            result.append(original_statements[i])

        result = self._group_constraints_with_same_prop_and_obj(result)
        result = self._group_constraints_with_same_prop_but_different_obj(result)

        result.sort(reverse=True, key=lambda x:x.probability)  # Restoring order completly
        return result


    def _group_constraints_with_same_prop_but_different_obj(self, candidate_statements):
        result = []
        already_visited = set()
        for i in range(0, len(candidate_statements)):
            a_statement = candidate_statements[i]
            if a_statement.st_property != RDF_TYPE_STR:
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
                        result.append(self._compose_statement_with_objects_in_or(group_to_decide))
            else:
                result.append(a_statement)
        return result


    def _group_constraints_with_same_prop_and_obj(self, candidate_statements):
        result = []
        already_visited = set()
        for i in range(0, len(candidate_statements)):
            a_statement = candidate_statements[i]
            if a_statement not in already_visited:
                already_visited.add(a_statement)
                group_to_decide = [a_statement]
                for j in range(i+1, len(candidate_statements)):
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


    def _compose_statement_with_objects_in_or(self, list_of_candidate_statements):
        list_of_candidate_statements.sort(reverse=True, key=lambda x: x.probability)
        composed_type = list_of_candidate_statements[0].st_type
        composed_probability = list_of_candidate_statements[0].probability
        for a_sentence in list_of_candidate_statements[1:]:
            composed_type += " OR " + a_sentence.st_type
            composed_probability += a_sentence.probability



        result = Statement(st_property=list_of_candidate_statements[0].st_property,
                           st_type=composed_type,
                           probability=composed_probability,
                           cardinality="+")

        for a_sentence in list_of_candidate_statements:
            for a_comment in a_sentence.comments:
                result.add_comment(a_comment)
                result.add_comment(self._turn_statement_into_comment(a_sentence))

        return result




    def _decide_best_statement_with_cardinalities_in_comments(self, list_of_candidate_statements):
        list_of_candidate_statements.sort(reverse=True, key=lambda x:x.probability)
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
        return self._probability_representation(a_statement.probability) + \
               " obj: " + a_statement.st_type + ". Cardinality: " + self._cardinality_representation(a_statement.cardinality)


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


    def _serialize_statement(self, a_statement, is_last_statement_of_shape):
        st_property = self._tune_token(a_statement.st_property)
        st_target_element = self._str_of_target_element(a_statement.st_type,
                                                        a_statement.st_property)
        cardinality = self._cardinality_representation(
            a_statement.cardinality)
        result = st_property + _SPACES_GAP_BETWEEN_TOKENS + st_target_element + _SPACES_GAP_BETWEEN_TOKENS + \
                 cardinality + self._closure_of_statement(is_last_statement_of_shape)

        result += self._adequate_amount_of_final_spaces(result)
        result += self._probability_representation(a_statement.probability)
        self._write_line(result, indent_level=1)
        for a_comment in a_statement.comments:
            self._write_line(a_comment, indent_level=4)


    def _str_of_target_element(self, target_element, st_property):
        """
        Special treatment for rdf:type. We build a value set with an specific URI
        :param target_element:
        :param st_property:
        :return:
        """
        if st_property == RDF_TYPE_STR:
            return "[" + self._tune_token(target_element) + "]"
        return target_element

    def _tune_token(self, a_token):
        for a_namespace in self._namespaces_dict:
            if a_namespace in a_token:
                return a_token.replace(a_namespace, self._namespaces_dict[a_namespace] + ":")
        return "<" + a_token + ">"

    def _probability_representation(self, probability):
        return _COMMENT_INI + str(probability * 100) + " %"

    def _cardinality_representation(self, cardinality):
        if cardinality == "+":
            return cardinality
        else:
            return "{" + str(cardinality) + "}"


    # def _cardinality_representation(self, cardinality):
    #     if cardinality == "1" or cardinality == 1:
    #         return ""
    #     return str(cardinality)


    def _closure_of_statement(self, is_last_statement):
        if is_last_statement:
            return ""
        return ";"


    def _adequate_amount_of_final_spaces(self, current_line):
        if len(current_line) > _TARGET_LINE_LENGHT - 10:
            return _SPACES_GAP_FOR_FREQUENCY
        result = ""
        for i in range(0, _TARGET_LINE_LENGHT - len(current_line)):
            result += " "
        return result


    def _serialize_shape_name(self, a_shape):
        self._write_line(a_shape.name.replace("@", ":"))


    def _serialize_opening_of_rules(self):
        self._write_line("{")


    def _serialize_closure_of_rule(self):
        self._write_line("}")


    def _serialize_shape_gap(self):
        self._write_line("")
        self._write_line("")
