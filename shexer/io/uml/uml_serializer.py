from plantuml import PlantUML
from shexer.utils.shapes import prefixize_shape_name_if_possible
from shexer.utils.uri import prefixize_uri_if_possible

class UMLSerializer(object):

    def __init__(self, shapes_list, url_server, image_path, namespaces_dict=None):
        self._shapes_list = shapes_list
        self._url_server = url_server
        self._image_path = image_path
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}

        self._diagram = None

        self._server_connection = self._init_server_connection()



    def serialize_shapes(self):

        self._reset_diagram()

        self._init_diagram()
        self._fill_diagram_with_shapes()
        self._close_diagram()
        result = self._send_diagram_to_server()
        self._store_diagram()

    def _send_diagram_to_server(self):
        pass  # TODO

    def _store_diagram(self):
        print(self._diagram)

    def _fill_diagram_with_shapes(self):
        self._declare_shapes_and_atts()
        self._declare_relations()


    def _declare_relations(self):
        for a_shape in self._shapes_list:
            for a_statement in a_shape.yield_statements():
                if  self._is_a_shape_link(a_statement):
                    origin_name = prefixize_shape_name_if_possible(a_shape_name=a_shape.name,
                                                                   namespaces_prefix_dict=self._namespaces_dict)
                    target_name = prefixize_shape_name_if_possible(a_shape_name=a_statement._st_type,
                                                                   namespaces_prefix_dict=self._namespaces_dict)
                    target_st = prefixize_uri_if_possible(target_uri=a_statement.st_property,
                                                          namespaces_prefix_dict=self._namespaces_dict,
                                                          corners=False)
                    self._write_line( f"{origin_name} --> {target_name} : {target_st}")

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
                target_obj =  prefixize_uri_if_possible(target_uri=a_statement.st_type,
                                                      namespaces_prefix_dict=self._namespaces_dict,
                                                      corners=False)

                self._write_line(f"{prop} : {target_obj} "
                                 + f" {str(a_statement.cardinality) if a_statement.cardinality != 1 else '' }")

    def _is_a_shape_link(self, statement):
        return statement.st_type.startswith("@")

    def _declare_and_open_shape(self, a_shape):
        target_name = prefixize_shape_name_if_possible(a_shape_name=a_shape.name,
                                                       namespaces_prefix_dict=self._namespaces_dict)
        self._write_line(f"class {target_name} {{")

    def _close_shape(self):
        self._write_line("}", spacing=True)

    def _reset_diagram(self):
        self._diagram = ""

    def _init_diagram(self):
        self._write_line("@startuml", spacing=True)

    def _close_diagram(self):
        self._write_line("@endum")

    def _write_line(self, text, spacing=False):
        self._diagram += text + "\n"* ( 1 if not spacing else 2)

    def _init_server_connection(self):
        return PlantUML(url=self._url_server)