from shexer.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from shexer.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS, KLEENE_CLOSURE, OPT_CARDINALITY


class FixedPropChoiceStatementSerializer(BaseStatementSerializer):

    def __init__(self, instantiation_property_str, frequency_serializer, disable_comments=False, is_inverse=False):
        super(FixedPropChoiceStatementSerializer, self).__init__(instantiation_property_str=instantiation_property_str,
                                                                 disable_comments=disable_comments,
                                                                 is_inverse=is_inverse,
                                                                 frequency_serializer=frequency_serializer)

    def serialize_statement_with_indent_level(self, a_statement, is_last_statement_of_shape, namespaces_dict):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, namespaces_dict)
        st_target_elements = []
        for a_type in a_statement.st_types:
            st_target_elements.append(self.str_of_target_element(target_element=a_type,
                                                                 st_property=a_statement.st_property,
                                                                 namespaces_dict=namespaces_dict))

        content_line = st_property + SPACES_GAP_BETWEEN_TOKENS
        content_line += (SPACES_GAP_BETWEEN_TOKENS + "OR" + SPACES_GAP_BETWEEN_TOKENS).join(st_target_elements)
        content_line += SPACES_GAP_BETWEEN_TOKENS + BaseStatementSerializer.cardinality_representation(
            statement=a_statement,
            out_of_comment=True)
        content_line += ";" if not is_last_statement_of_shape else ""
        tuples_line_indent.append((content_line, 1))


        for a_comment in a_statement.comments:
            tuples_line_indent.append((a_comment, 4))
        return tuples_line_indent


    @staticmethod
    def turn_statement_into_comment(statement, namespaces_dict):
        return statement.probability_representation() + \
               " with cardinality " + statement.cardinality_representation()
