from plantuml import PlantUML

class UMLSerializer(object):

    def __init__(self, shapes_list, url_server, image_path):
        self._shapes_list = shapes_list
        self._url_server = url_server
        self._image_path = image_path

        self._diagram = None

        self._server_connection = self._init_server_connection()



    def serialize_shapes(self):

        self._reset_diagram()

        self._init_diagram()
        self._fill_diagram_with_shapes()
        self._close_diagram()
        result = self._send_diagram_to_server()
        self._store_diagram()

    def _fill_diagram_with_shapes(self):
        self._declare_shapes_and_atts()
        self._declare_relations()
        # TODO : CONTINUE IMPLEMENTING THESE FUNCTIONS



    def _reset_diagram(self):
        self._diagram = ""

    def _init_diagram(self):
        self._write_line("@startuml")

    def _close_diagram(self):
        self._write_line("@endum")

    def _write_line(self, text):
        self._diagram += text + "\n"

    def _init_server_connection(self):
        return PlantUML(url=self._url_server)