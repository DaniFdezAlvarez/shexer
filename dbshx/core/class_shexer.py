import json
from dbshx.model.statement import Statement


class ClassShexer (object):

    def __init__(self, class_counts_dict, class_profile_dict=None, class_profile_json_file=None):
        self._class_counts_dict = class_counts_dict
        self._class_profile_dict = class_profile_dict if class_profile_dict is not None else self._load_class_profile_dict_from_file(class_profile_json_file)
        self._shapes_dict = {}

    def shex_classes(self):
        self._build_shapes()
        self._sort_shapes()
        return self._shapes_dict


    def _build_shapes(self):
        for a_class_key in self._class_profile_dict:
            name = self._build_authomatic_name_for_class_uri(a_class_key)
            number_of_instances = self._class_counts_dict[a_class_key]
            # TODO Ojo cuidao aqui. Metemos shapes o que metemos en el resultado
            statements = []
            for a_prop_key in self._class_profile_dict[a_class_key]:
                for a_type_key in self._class_profile_dict[a_class_key][a_prop_key]:
                    for a_cardinality in self._class_profile_dict[a_class_key][a_prop_key][a_type_key]:
                        statements.append("")  # TODO construir Statements


    def _build_authomatic_name_for_class_uri(self, class_uri):
        if "#" in class_uri and class_uri[-1] != "#":
            return "@" + class_uri[class_uri.rfind("#")+1:]
        if "/" in class_uri:
            if class_uri[-1] != "/":
                return "@" + class_uri[class_uri.rfind("/")+1:]
            else:
                return "@" + class_uri[class_uri[:-1].rfind("/") + 1:]
        else:
            return "@" + class_uri

    @staticmethod
    def _load_class_profile_dict_from_file(source_file):
        with open(source_file, "r") as in_stream:
            return json.load(in_stream)