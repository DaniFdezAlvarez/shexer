from dbshx.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer

class Statement(object):

    def __init__(self, st_property, st_type, cardinality, probability,
                 comments=None, static_ref_to_serialize=BaseStatementSerializer):
        self._st_property = st_property
        self._st_type = st_type
        self._cardinality = cardinality
        self._probability = probability
        self._static_ref_to_serialize = static_ref_to_serialize
        self._comments = [] if comments is None else comments

    def get_tuples_to_serialize_line_indent_level(self, is_last_statement_of_shape, namespaces_dict):
        return self._static_ref_to_serialize.\
            serialize_statement_with_indent_level(a_statement=self,
                                                  is_last_statement_of_shape= is_last_statement_of_shape,
                                                  namespaces_dict=namespaces_dict)

    def add_comment(self, comment):
        self._comments.append(comment)

    @property
    def st_property(self):
        return self._st_property

    @property
    def st_type(self):
        return self._st_type

    @property
    def cardinality(self):
        return self._cardinality

    @property
    def probability(self):
        return self._probability

    @property
    def comments(self):
        return self._comments
