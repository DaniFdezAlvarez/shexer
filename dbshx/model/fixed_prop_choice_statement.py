from dbshx.model.statement import Statement

class FixedPropChoiceStatement(Statement):

    def __init__(self, st_property, st_types, cardinality, probability):
        super(FixedPropChoiceStatement, self).__init__(st_property, None, cardinality, probability)
        self._st_types = st_types

    @property
    def st_type(self):
        raise TypeError("Choice statements doesnt have a single type")

    @property
    def st_types(self):
        return self._st_types