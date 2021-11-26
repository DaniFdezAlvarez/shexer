from shexer.core.shexing.strategy.asbtract_shexing_strategy import AbstractShexingStrategy
from shexer.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from shexer.io.shex.formater.statement_serializers.fixed_prop_choice_statement_serializer import \
    FixedPropChoiceStatementSerializer  # TODO: REPFACTOR
from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.model.statement import Statement
from shexer.model.shape import Shape

class DirectShexingStrategy(AbstractShexingStrategy):

    def __init__(self, class_shexer):
        super().__init__(class_shexer)
        self._class_profile_dict = self._class_shexer._class_profile_dict
        self._shapes_namespace = self._class_shexer._shapes_namespace
        self._class_counts_dict = self._class_shexer._class_counts_dict

    def remove_statements_to_gone_shapes(self, shape, shape_names_to_remove):
        shape.statements = self._statements_without_shapes_to_remove(original_statements=shape.statements,
                                                                     shape_names_to_remove=shape_names_to_remove)

    def set_valid_shape_constraints(self, shape):
        valid_statements = self._select_valid_statements_of_shape(shape.statements)
        self._tune_list_of_valid_statements(valid_statements=valid_statements)
        shape.statements = valid_statements


    def yield_base_shapes(self, acceptance_threshold):
        for a_class_key in self._class_profile_dict:
            name = build_shapes_name_for_class_uri(class_uri=a_class_key,
                                                   shapes_namespace=self._shapes_namespace)
            number_of_instances = float(self._class_counts_dict[a_class_key])
            statements = []
            for a_prop_key in self._class_profile_dict[a_class_key]:
                for a_type_key in self._class_profile_dict[a_class_key][a_prop_key]:
                    for a_cardinality in self._class_profile_dict[a_class_key][a_prop_key][a_type_key]:
                        frequency = self._compute_frequency(number_of_instances,
                                                            self._class_profile_dict
                                                            [a_class_key]
                                                            [a_prop_key]
                                                            [a_type_key]
                                                            [a_cardinality])
                        if frequency >= acceptance_threshold:
                            statements.append(Statement(st_property=a_prop_key,
                                                        st_type=a_type_key,
                                                        cardinality=a_cardinality,
                                                        probability=frequency))

            yield Shape(name=name,
                        class_uri=a_class_key,
                        statements=statements)

    def _set_serializer_object_for_statements(self, statement):
        statement.serializer_object = BaseStatementSerializer(
            instantiation_property_str=self._instantiation_property_str,
            disable_comments=self._disable_comments)

    def _get_serializer_for_choice_statement(self):
        return FixedPropChoiceStatementSerializer(
            instantiation_property_str=self._instantiation_property_str,
            disable_comments=self._disable_comments)