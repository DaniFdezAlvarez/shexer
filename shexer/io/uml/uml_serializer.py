from plantuml import PlantUML
from shexer.utils.shapes import prefixize_shape_name_if_possible
from shexer.utils.uri import prefixize_uri_if_possible
from shexer.model.fixed_prop_choice_statement import FixedPropChoiceStatement
from shexer.consts import RDF_TYPE
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME
import warnings


class UMLSerializer(object):

    def __init__(self, shapes_list, url_server, image_path, namespaces_dict=None, instantiation_property=RDF_TYPE):
        self._disable_connection_warnings()
        self._shapes_list = shapes_list
        self._url_server = url_server
        self._image_path = image_path
        self._instantiation_property = instantiation_property
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}

        self._shape_alias = {}

        self._diagram = None

        self._server_connection = self._init_server_connection()

    def serialize_shapes(self):

        self._reset_diagram()

        self._init_diagram()
        self._fill_diagram_with_shapes()
        self._close_diagram()
        result = self._send_diagram_to_server()
        self._store_diagram(result)

    def _disable_connection_warnings(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def _send_diagram_to_server(self):
        return self._server_connection.processes(self._diagram)


    def _store_diagram(self, img_diagram):
        with open(self._image_path, "wb") as out_stream:
            out_stream.write(img_diagram)


    def _fill_diagram_with_shapes(self):
        self._declare_shapes_and_atts()
        self._declare_relations()

    def _declare_relations(self):
        for a_shape in self._shapes_list:
            for a_statement in a_shape.yield_statements():
                if self._is_a_shape_link(a_statement):
                    origin_name = prefixize_shape_name_if_possible(a_shape_name=a_shape.name,
                                                                   namespaces_prefix_dict=self._namespaces_dict)
                    target_name = prefixize_shape_name_if_possible(a_shape_name=a_statement._st_type,
                                                                   namespaces_prefix_dict=self._namespaces_dict)
                    target_st = prefixize_uri_if_possible(target_uri=a_statement.st_property,
                                                          namespaces_prefix_dict=self._namespaces_dict,
                                                          corners=False)
                    self._write_line(
                        f"{self._shape_alias[origin_name]} --> {self._shape_alias[target_name]} : {target_st}")

    def _declare_shapes_and_atts(self):
        for a_shape in self._shapes_list:
            self._declare_and_open_shape(a_shape)
            self._declare_shape_atts(a_shape)
            self._close_shape()

    def _declare_shape_atts(self, a_shape):
        for a_statement in a_shape.yield_statements():
            if not self._is_a_shape_link(a_statement):
                prop = prefixize_uri_if_possible(target_uri=a_statement.st_property,
                                                 namespaces_prefix_dict=self._namespaces_dict,
                                                 corners=False)
                target_obj = self._serialize_obj_of_non_shape_link(a_statement)

                self._write_line(f"{prop} : {target_obj}"
                                 + f" {str(a_statement.cardinality) if a_statement.cardinality != 1 else ''}")


    def _serialize_obj_of_non_shape_link(self, a_statement):
        if not type(a_statement) == FixedPropChoiceStatement:
            result = prefixize_uri_if_possible(target_uri=a_statement.st_type,
                                         namespaces_prefix_dict=self._namespaces_dict,
                                         corners=False)
            if self._is_a_type_declaration(a_statement):
                result = "[" + result + "]"
            return result
        types = []
        for a_type in a_statement.st_types:
            if a_type.startswith(STARTING_CHAR_FOR_SHAPE_NAME):
                types.append("@" + prefixize_uri_if_possible(target_uri=a_type[1:],
                                                             namespaces_prefix_dict=self._namespaces_dict,
                                                             corners=True))
            else:
                types.append(a_type)  # It should be IRI
        return " OR ".join(types)

    def _is_a_type_declaration(self, a_statement):
        return a_statement.st_property == self._instantiation_property

    def _is_a_shape_link(self, statement):
        if type(statement) == FixedPropChoiceStatement:
            return False
        return statement.st_type.startswith(STARTING_CHAR_FOR_SHAPE_NAME)

    def _declare_and_open_shape(self, a_shape):
        target_name = prefixize_shape_name_if_possible(a_shape_name=a_shape.name,
                                                       namespaces_prefix_dict=self._namespaces_dict)
        if ":" in target_name or "-" in target_name or target_name.startswith("<") :
            self._declare_shape_with_alias(target_name)
        else:
            self._declare_shape_without_alias(target_name)

    def _declare_shape_without_alias(self, target_name):
        self._shape_alias[target_name] = target_name
        self._write_line(f"object {target_name} {{")

    def _declare_shape_with_alias(self, target_name):
        alias = target_name
        alias = alias.replace(":", "_")
        alias = alias.replace("-", "_")

        if alias.startswith("<"):
            alias = target_name[1:-1]
        self._shape_alias[target_name] = alias
        self._write_line(f'object "{target_name}" as {alias} {{')

    def _close_shape(self):
        self._write_line("}", spacing=True)

    def _reset_diagram(self):
        self._diagram = ""

    def _init_diagram(self):
        self._write_line("@startuml", spacing=True)

    def _close_diagram(self):
        self._write_line("@enduml")

    def _write_line(self, text, spacing=False):
        self._diagram += text + "\n" * (1 if not spacing else 2)

    def _init_server_connection(self):
        return PlantUML(url=self._url_server)


