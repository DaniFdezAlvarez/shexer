from shexer.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer, \
    SPACES_GAP_BETWEEN_TOKENS

#
# class InverseStatementSerializer(BaseStatementSerializer):
#
#     def __init__(self, ref_statement_serializer):
#         super().__init__(ref_statement_serializer._instantiation_property_str)
#         self._ref_statement_serializer = ref_statement_serializer
#
#     def serialize_statement_with_indent_level(self, a_statement, is_last_statement_of_shape, namespaces_dict):
#         base_result = super().serialize_statement_with_indent_level(
#             a_statement=a_statement,
#             is_last_statement_of_shape=is_last_statement_of_shape,
#             namespaces_dict=namespaces_dict)
#         if len(base_result) == 0:
#             return base_result
#         self._add_inverse_sense_to_first_tuple(base_result)
#         return base_result
#
#     def _add_inverse_sense_to_first_tuple(self, statement_str_indent_tuples):
#         """
#         This method modifies the input, no return needed.
#         :param statement_str_indent_tuples:
#         :return:
#         """
#         statement_str_indent_tuples[0][0] = _INVERSE_SENSE_SHEXC + \
#                                             SPACES_GAP_BETWEEN_TOKENS + \
#                                             statement_str_indent_tuples[0][0]
#
#     def _sense_flag(self):
#         return _INVERSE_SENSE_SHEXC + SPACES_GAP_BETWEEN_TOKENS
