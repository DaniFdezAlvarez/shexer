class Statement(object):

    def __init__(self, st_property, st_type, cardinality, probability,
                 comments=None, serializer_object=None):
        self._st_property = st_property
        self._st_type = st_type
        self._cardinality = cardinality
        self._probability = probability
        self._serializer_object = serializer_object
        self._comments = [] if comments is None else comments

    def get_tuples_to_serialize_line_indent_level(self, is_last_statement_of_shape, namespaces_dict):
        return self._serializer_object.\
            serialize_statement_with_indent_level(a_statement=self,
                                                  is_last_statement_of_shape= is_last_statement_of_shape,
                                                  namespaces_dict=namespaces_dict)

    def probability_representation(self):
        return self._serializer_object.probability_representation(self._probability)

    def cardinality_representation(self):
        return self._serializer_object.cardinality_representation(self._cardinality)

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

    @property
    def serializer_object(self):
        return self._serializer_object

    @serializer_object.setter
    def serializer_object(self, value):
        self._serializer_object = value
