from shexer.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS, \
    COMMENT_INI, TARGET_LINE_LENGHT, SPACES_GAP_FOR_FREQUENCY, KLEENE_CLOSURE, POSITIVE_CLOSURE
from shexer.model.IRI import IRI_ELEM_TYPE
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME



class BaseStatementSerializer(object):

    def __init__(self, instantiation_property_str):
        self._instantiation_property_str = instantiation_property_str


    def serialize_statement_with_indent_level(self, a_statement, is_last_statement_of_shape, namespaces_dict):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, namespaces_dict)
        st_target_element = self.str_of_target_element(target_element=a_statement.st_type,
                                                       st_property=a_statement.st_property,
                                                       namespaces_dict=namespaces_dict)
        cardinality = BaseStatementSerializer.cardinality_representation(
            cardinality=a_statement.cardinality,
            statement=a_statement,
            out_of_comment=True)
        result = st_property + SPACES_GAP_BETWEEN_TOKENS + st_target_element + SPACES_GAP_BETWEEN_TOKENS + \
                 cardinality + BaseStatementSerializer.closure_of_statement(is_last_statement_of_shape)

        if a_statement.cardinality != KLEENE_CLOSURE:
            result += BaseStatementSerializer.adequate_amount_of_final_spaces(result)
            result += BaseStatementSerializer.probability_representation(a_statement.probability)
        tuples_line_indent.append((result, 1))

        for a_comment in a_statement.comments:
            tuples_line_indent.append((a_comment, 4))

        return tuples_line_indent


    def str_of_target_element(self, target_element, st_property, namespaces_dict):
        """
        Special treatment for instantiation_property. We build a value set with an specific URI
        :param target_element:
        :param st_property:
        :return:
        """
        if st_property == self._instantiation_property_str:
            return "[" + BaseStatementSerializer.tune_token(target_element, namespaces_dict) + "]"
        return BaseStatementSerializer.tune_token(target_element, namespaces_dict)


    @staticmethod
    def tune_token(a_token, namespaces_dict):
        # TODO:  a lot to correct here for normal behaviour
        if a_token == IRI_ELEM_TYPE: # iri
            return a_token
        if a_token.startswith(STARTING_CHAR_FOR_SHAPE_NAME):  # Shape
            return "@:" + a_token.replace(STARTING_CHAR_FOR_SHAPE_NAME, "")

        for a_namespace in namespaces_dict:  # Prefixed element (all literals are prefixed elements)
            if a_namespace in a_token:
                return a_token.replace(a_namespace, namespaces_dict[a_namespace] + ":")

        return "<" + a_token + ">"  # Complete URIs


    @staticmethod
    def probability_representation(probability):
        return COMMENT_INI + str(probability * 100) + " %"


    @staticmethod
    def cardinality_representation(cardinality, statement, out_of_comment=False):
        if out_of_comment and statement.cardinality == 1:
            return ""
        if cardinality in [POSITIVE_CLOSURE, KLEENE_CLOSURE]:
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
