from dbshx.io.shex.formater.shex_serializer import SPACES_GAP_BETWEEN_TOKENS, \
    COMMENT_INI, TARGET_LINE_LENGHT, SPACES_GAP_FOR_FREQUENCY
from dbshx.core.class_profiler import RDF_TYPE_STR



class BaseStatementSerializer(object):

    @staticmethod
    def serialize_statement_with_indent_level(a_statement, is_last_statement_of_shape, namespaces_dict):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, namespaces_dict)
        st_target_element = BaseStatementSerializer.str_of_target_element(target_element=a_statement.st_type,
                                                                          st_property=a_statement.st_property,
                                                                          namespaces_dict=namespaces_dict)
        cardinality = BaseStatementSerializer.cardinality_representation(
            a_statement.cardinality)
        result = st_property + SPACES_GAP_BETWEEN_TOKENS + st_target_element + SPACES_GAP_BETWEEN_TOKENS + \
                 cardinality + BaseStatementSerializer.closure_of_statement(is_last_statement_of_shape)

        result += BaseStatementSerializer.adequate_amount_of_final_spaces(result)
        result += BaseStatementSerializer.probability_representation(a_statement.probability)
        tuples_line_indent.append((result, 1))
        for a_comment in a_statement.comments:
            tuples_line_indent.append((a_comment, 4))

        return tuples_line_indent


    @staticmethod
    def str_of_target_element(target_element, st_property, namespaces_dict):
        """
        Special treatment for rdf:type. We build a value set with an specific URI
        :param target_element:
        :param st_property:
        :return:
        """
        if st_property == RDF_TYPE_STR:
            return "[" + BaseStatementSerializer.tune_token(target_element, namespaces_dict) + "]"
        return BaseStatementSerializer.tune_token(target_element, namespaces_dict)


    @staticmethod
    def tune_token(a_token, namespaces_dict):
        for a_namespace in namespaces_dict:
            if a_namespace in a_token:
                return a_token.replace(a_namespace, namespaces_dict[a_namespace] + ":")
        return "<" + a_token + ">"


    @staticmethod
    def probability_representation(probability):
        return COMMENT_INI + str(probability * 100) + " %"


    @staticmethod
    def cardinality_representation(cardinality):
        if cardinality == "+":
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