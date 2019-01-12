from dbshx.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from dbshx.io.shex.formater.shex_serializer import SPACES_GAP_BETWEEN_TOKENS


class FixedPropChoiceStatementSerializer(BaseStatementSerializer):

    def __init__(self):
        pass

    @staticmethod
    def serialize_statement_with_indent_level(a_statement, is_last_statement_of_shape, namespaces_dict):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, namespaces_dict)
        st_target_elements = []
        for a_type in a_statement.st_types:
            st_target_elements.append(BaseStatementSerializer.str_of_target_element(target_element=a_type,
                                                                                    st_property=a_statement.st_property,
                                                                                    namespaces_dict=namespaces_dict))
        cardinality = BaseStatementSerializer.cardinality_representation(
            a_statement.cardinality)

        tuples_line_indent.append(FixedPropChoiceStatementSerializer._opening_tuple_line_of_choice())

        tuples_line_indent.append(FixedPropChoiceStatementSerializer._statement_in_choice_no_cardinality(st_property,
                                                                                                         st_target_elements[0]))

        # TODO CONTINUE HERE

        result = st_property + SPACES_GAP_BETWEEN_TOKENS + st_target_element + SPACES_GAP_BETWEEN_TOKENS + \
                 cardinality + BaseStatementSerializer.closure_of_statement(is_last_statement_of_shape)

        result += BaseStatementSerializer.adequate_amount_of_final_spaces(result)
        result += BaseStatementSerializer.probability_representation(a_statement.probability)
        tuples_line_indent.append((result, 1))
        for a_comment in a_statement.comments:
            tuples_line_indent.append((a_comment, 4))

        return tuples_line_indent


    @staticmethod
    def _opening_tuple_line_of_choice():
        return "(", 1

    @staticmethod
    def _statement_in_choice_no_cardinality(st_property, st_type):
        return (st_property + SPACES_GAP_BETWEEN_TOKENS + st_type ,1)