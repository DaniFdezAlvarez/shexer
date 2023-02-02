from shexer.model.statement import Statement

class FixedPropChoiceStatement(Statement):

    def __init__(self, st_property, st_types, cardinality, n_occurences, probability, comments=None,
                 serializer_object=None, is_inverse=False):
        super(FixedPropChoiceStatement, self).__init__(st_property=st_property,
                                                       st_type=None,
                                                       cardinality=cardinality,
                                                       n_occurences=n_occurences,
                                                       probability=probability,
                                                       comments=comments,
                                                       serializer_object=serializer_object,
                                                       is_inverse=is_inverse)
        self._st_types = st_types

    @property
    def st_type(self):
        raise TypeError("Choice statements doesnt have a single type")

    @property
    def st_types(self):
        return self._st_types