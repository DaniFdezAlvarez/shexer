from shexer.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from shexer.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS, KLEENE_CLOSURE, OPT_CARDINALITY


class FixedPropChoiceStatementSerializer(BaseStatementSerializer):

    def __init__(self, instantiation_property_str, disable_comments=False):
        super(FixedPropChoiceStatementSerializer, self).__init__(instantiation_property_str=instantiation_property_str,
                                                                 disable_comments=disable_comments)

    def serialize_statement_with_indent_level(self, a_statement, is_last_statement_of_shape, namespaces_dict):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, namespaces_dict)
        st_target_elements = []
        for a_type in a_statement.st_types:
            st_target_elements.append(self.str_of_target_element(target_element=a_type,
                                                                 st_property=a_statement.st_property,
                                                                 namespaces_dict=namespaces_dict))

        tuples_line_indent.append(FixedPropChoiceStatementSerializer._opening_tuple_line_of_choice())

        tuples_line_indent.append(FixedPropChoiceStatementSerializer.
                                  _statement_in_choice_no_cardinality(st_property,
                                                                      st_target_elements[0]))

        for a_type in st_target_elements[1:]:
            tuples_line_indent.append(FixedPropChoiceStatementSerializer._tuple_of_disjunction())
            tuples_line_indent.append(
                FixedPropChoiceStatementSerializer._statement_in_choice_no_cardinality(st_property,
                                                                                       a_type))

        tuples_line_indent.append(self._tuple_closing_choice(a_statement,
                                                             is_last_statement_of_shape))

        for a_comment in a_statement.comments:
            tuples_line_indent.append((a_comment, 4))
        a = 3 + 1

        return tuples_line_indent


    def _tuple_closing_choice(self, a_statement, is_last_statement_of_shape):
        str_res = ")" + SPACES_GAP_BETWEEN_TOKENS + \
                  BaseStatementSerializer.cardinality_representation(cardinality=a_statement.cardinality,
                                                                     statement=a_statement,
                                                                     out_of_comment=True) + \
                  BaseStatementSerializer.closure_of_statement(is_last_statement_of_shape)

        if a_statement.cardinality not in [KLEENE_CLOSURE, OPT_CARDINALITY] and not self._disable_comments:
            str_res += BaseStatementSerializer.adequate_amount_of_final_spaces(str_res) + \
                       BaseStatementSerializer.probability_representation(a_statement.probability)
        return str_res, 1

    @staticmethod
    def _tuple_of_disjunction():
        return "|", 2

    @staticmethod
    def _opening_tuple_line_of_choice():
        return "(", 1

    @staticmethod
    def _statement_in_choice_no_cardinality(st_property, st_type):
        return (st_property + SPACES_GAP_BETWEEN_TOKENS + st_type, 1)

    @staticmethod
    def turn_statement_into_comment(statement, namespaces_dict):
        return statement.probability_representation() + \
               " with cardinality " + statement.cardinality_representation()
