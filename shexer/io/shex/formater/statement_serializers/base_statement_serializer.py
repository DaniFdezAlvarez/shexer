from shexer.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS, \
    COMMENT_INI, TARGET_LINE_LENGHT, SPACES_GAP_FOR_FREQUENCY, KLEENE_CLOSURE, POSITIVE_CLOSURE, OPT_CARDINALITY
from shexer.model.IRI import IRI_ELEM_TYPE
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME
from shexer.utils.shapes import prefixize_shape_name_if_possible

_INVERSE_SENSE_SHEXC = "^"

class BaseStatementSerializer(object):

    def __init__(self, instantiation_property_str, frequency_serializer, disable_comments=False, is_inverse=False):
        self._instantiation_property_str = instantiation_property_str
        self._disable_comments = disable_comments
        self._is_inverse = is_inverse
        self._frequency_serializer = frequency_serializer

    def serialize_statement_with_indent_level(self, a_statement, is_last_statement_of_shape, namespaces_dict):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, namespaces_dict)
        st_target_element = self.str_of_target_element(target_element=a_statement.st_type,
                                                       st_property=a_statement.st_property,
                                                       namespaces_dict=namespaces_dict)
        cardinality = BaseStatementSerializer.cardinality_representation(
            statement=a_statement,
            out_of_comment=True)
        result = self._sense_flag() + st_property + SPACES_GAP_BETWEEN_TOKENS + st_target_element + SPACES_GAP_BETWEEN_TOKENS + \
                 cardinality + BaseStatementSerializer.closure_of_statement(is_last_statement_of_shape)

        if a_statement.cardinality not in [KLEENE_CLOSURE, OPT_CARDINALITY] and not self._disable_comments:
            result += BaseStatementSerializer.adequate_amount_of_final_spaces(result)
            result += a_statement.probability_representation()
        tuples_line_indent.append((result, 1))

        for a_comment in a_statement.comments:
            tuples_line_indent.append((a_comment, 4))

        return tuples_line_indent

    def str_of_target_element(self, target_element, st_property, namespaces_dict):
        """
        Special treatment for instantiation_property. We build a value set with an specific URI
        :param target_element:
        :param st_property:
        :param namespaces_dict:
        :return:
        """
        if st_property == self._instantiation_property_str:
            return "[" + BaseStatementSerializer.tune_token(target_element, namespaces_dict) + "]"
        return BaseStatementSerializer.tune_token(target_element, namespaces_dict)

    @staticmethod
    def tune_token(a_token, namespaces_dict):
        # TODO:  a lot to correct here for normal behaviour
        if a_token.startswith(STARTING_CHAR_FOR_SHAPE_NAME):  # Shape
            # return STARTING_CHAR_FOR_SHAPE_NAME +":" + a_token.replace(STARTING_CHAR_FOR_SHAPE_NAME, "")
            return STARTING_CHAR_FOR_SHAPE_NAME \
                   + prefixize_shape_name_if_possible(a_shape_name=a_token,
                                                      namespaces_prefix_dict=namespaces_dict)
        if a_token == IRI_ELEM_TYPE:  # iri
            return a_token
        if ":" not in a_token:
            if "<" in a_token:
                return STARTING_CHAR_FOR_SHAPE_NAME + a_token
            else:
                return STARTING_CHAR_FOR_SHAPE_NAME + "<" + a_token + ">"
        candidate_prefixed = BaseStatementSerializer._prefixize_uri_if_possible(uri=a_token,
                                                                                namespaces_dict=namespaces_dict)
        if candidate_prefixed is not None:
            return candidate_prefixed

        return "<" + a_token + ">"  # Complete URIs

    @staticmethod
    def _prefixize_uri_if_possible(uri, namespaces_dict):
        """
        It returns None it it doesnt find an adequate prefix

        :param uri:
        :param namespaces_dict:
        :return:
        """
        best_match = None
        for a_namespace in namespaces_dict:  # Prefixed element (all literals are prefixed elements)
            if uri.startswith(a_namespace):
                if "/" not in uri[len(a_namespace):] and \
                        "#" not in uri[len(a_namespace):]:
                    best_match = a_namespace
                    break

        return None if best_match is None else uri.replace(best_match, namespaces_dict[best_match] + ":")


    def probability_representation(self, statement):
        return COMMENT_INI + self._frequency_serializer.serialize_frequency(statement)

    @staticmethod
    def cardinality_representation(statement, out_of_comment=False):
        cardinality = statement.cardinality
        if out_of_comment and cardinality == 1:
            return ""
        if cardinality in [POSITIVE_CLOSURE, KLEENE_CLOSURE, OPT_CARDINALITY]:
            return cardinality
        else:
            return "{" + str(cardinality) + "}"

    @staticmethod
    def closure_of_statement(is_last_statement):
        if is_last_statement:
            return ""
        return ";"

    @staticmethod
    def adequate_amount_of_final_spaces(current_line):
        if len(current_line) > TARGET_LINE_LENGHT - 10:
            return SPACES_GAP_FOR_FREQUENCY
        result = ""
        for i in range(0, TARGET_LINE_LENGHT - len(current_line)):
            result += " "
        return result

    @staticmethod
    def turn_statement_into_comment(statement, namespaces_dict):
        return statement.probability_representation() + \
               " obj: " + BaseStatementSerializer.tune_token(statement.st_type,
                                                             namespaces_dict) + \
               ". Cardinality: " + statement.cardinality_representation()

    def _sense_flag(self):
        return "" if not self._is_inverse else _INVERSE_SENSE_SHEXC + SPACES_GAP_BETWEEN_TOKENS
