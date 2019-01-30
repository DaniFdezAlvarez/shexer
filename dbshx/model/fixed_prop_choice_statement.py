from dbshx.model.statement import Statement
from dbshx.io.shex.formater.statement_serializers.fixed_prop_choice_statement_serializer import FixedPropChoiceStatementSerializer

class FixedPropChoiceStatement(Statement):

    def __init__(self, st_property, st_types, cardinality, probability, comments=None,
                 static_ref_to_serialize=FixedPropChoiceStatementSerializer):
        super(FixedPropChoiceStatement, self).__init__(st_property=st_property,
                                                       st_type=None,
                                                       cardinality=cardinality,
                                                       probability=probability,
                                                       comments=comments,
                                                       static_ref_to_serialize=static_ref_to_serialize)
        self._st_types = st_types

    @property
    def st_type(self):
        raise TypeError("Choice statements doesnt have a single type")

    @property
    def st_types(self):
        return self._st_types