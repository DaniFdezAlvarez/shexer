import json
from shexer.model.statement import Statement
from shexer.model.shape import Shape
from shexer.utils.shapes import build_shapes_name_for_class_uri


class ClassShexer (object):

    def __init__(self, class_counts_dict, class_profile_dict=None, class_profile_json_file=None):
        self._class_counts_dict = class_counts_dict
        self._class_profile_dict = class_profile_dict if class_profile_dict is not None else self._load_class_profile_dict_from_file(class_profile_json_file)
        self._shapes_list = []

    def shex_classes(self):
        self._build_shapes()
        self._sort_shapes()
        return self._shapes_list


    def _build_shapes(self):
        for a_class_key in self._class_profile_dict:
            name = build_shapes_name_for_class_uri(a_class_key)
            number_of_instances = float(self._class_counts_dict[a_class_key])
            # TODO Ojo cuidao aqui. Metemos shapes o que metemos en el resultado
            statements = []
            for a_prop_key in self._class_profile_dict[a_class_key]:
                for a_type_key in self._class_profile_dict[a_class_key][a_prop_key]:
                    for a_cardinality in self._class_profile_dict[a_class_key][a_prop_key][a_type_key]:
                        statements.append(Statement(st_property=a_prop_key,
                                                    st_type=a_type_key,
                                                    cardinality=a_cardinality,
                                                    probability=self._compute_frequency(number_of_instances,
                                                                                        self._class_profile_dict
                                                                                        [a_class_key]
                                                                                        [a_prop_key]
                                                                                        [a_type_key]
                                                                                        [a_cardinality])))

            a_shape = Shape(name=name,
                            class_uri=a_class_key,
                            statements=statements)
            self._shapes_list.append(a_shape)


    def _sort_shapes(self):
        for a_shape in self._shapes_list:
            a_shape.sort_statements(reverse=True,
                                    callback=self._value_to_compare_statements)

    def _value_to_compare_statements(self, a_statement):
        return a_statement.probability

    def _compute_frequency(self, number_of_instances, n_ocurrences_statement):
        return float(n_ocurrences_statement) / number_of_instances


    @staticmethod
    def _load_class_profile_dict_from_file(source_file):
        with open(source_file, "r") as in_stream:
            return json.load(in_stream)