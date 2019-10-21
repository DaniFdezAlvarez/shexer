from shexer.utils.file import load_whole_file_content
from shexer.model.shape_map import ShapeMap, ShapeMapItem
from shexer.io.shape_map.node_selector.node_selector_parser import NodeSelectorParser
from shexer.io.shape_map.label.shape_map_label_parser import ShapeMapLabelParser
from shexer.utils.dict import reverse_keys_and_values

class ShapeMapParser(object):

    def __init__(self, namespaces_prefix_dict, sgraph):
        reversed_dict = reverse_keys_and_values(namespaces_prefix_dict)
        self._node_selector_parser = NodeSelectorParser(prefix_namespaces_dict=reversed_dict,
                                                        sgraph=sgraph)
        self._label_parser = ShapeMapLabelParser(prefix_namespaces_dict=reversed_dict)
        self._sgraph = sgraph

    def parse_shape_map(self, source_file=None, raw_content=None):
        self._check_input(source_file, raw_content)
        target_content = raw_content
        if source_file is not None:
            target_content = load_whole_file_content(source_file)
        return self._parse_shape_map_from_str(target_content)

    @staticmethod
    def _check_input(source_file, raw_content):
        if (source_file is None) == (raw_content is None):
            raise ValueError("Yoy must provide exactly one kind of input")

    def _parse_shape_map_from_str(self, raw_content):
        raise NotImplementedError("Implement this in derived classes")


####################################################

from shexer.io.json.json_loader import load_string_json

_KEY_NODE_SELECTOR = "nodeSelector"
_KEY_LABEL = "shapeLabel"


class JsonShapeMapParser(ShapeMapParser):
    """
    WARNING!! This is a toy parser. We are assuming many wel--formed stuff
    for the structure of the json itself and for the shape labels.
    Node selectors are well checked

    Example of expected format:
    [
  { "nodeSelector": "<http://data.example/node1>",
    "shapeLabel": "<http://schema.example/Shape2>"
    },
  { "nodeSelector": "<http://data.example/node1>",
    "shapeLabel": "<http://schema.example/Shape2>"
    }
]
    """

    def __init__(self, namespaces_prefix_dict, sgraph):
        super().__init__(namespaces_prefix_dict=namespaces_prefix_dict,
                         sgraph=sgraph)

    def _parse_shape_map_from_str(self, raw_content):
        result = ShapeMap()
        json_obj = load_string_json(raw_content)
        for a_list_elem in json_obj:
            result.add_item(ShapeMapItem(
                node_selector=self._node_selector_parser.parse_node_selector(a_list_elem[_KEY_NODE_SELECTOR]),
                shape_label=self._label_parser.parse_shape_map_label(a_list_elem[_KEY_LABEL])
            )
            )
        return result


####################################################


from shexer.io.line_reader.raw_string_line_reader import RawStringLineReader


class FixedShapeMapParser(ShapeMapParser):
    """
    WARNING!!!     This is a toy parser.

    Currently, this parser of Fixed ShapeMap syntax requires each couple selector@label to be in separate lines.
    Also, It will just assume trailing commas at the end of the line. If they are there, thats OK. If not, it will
    assume that its just because it is the last element.
    """

    def __init__(self, namespaces_prefix_dict, sgraph):
        super().__init__(namespaces_prefix_dict=namespaces_prefix_dict,
                         sgraph=sgraph)

    def _parse_shape_map_from_str(self, raw_content):
        result = ShapeMap()
        for a_line in RawStringLineReader(raw_string=raw_content).read_lines():
            a_line = a_line.strip()
            if not self._is_an_empty_line(a_line):
                result.add_item(self._parse_shape_map_item_from_line(a_line))

        return result

    def _is_an_empty_line(self, line):
        """
        It is expecting to receive a line which has already been stripped ()
        :param line:
        :return:
        """
        if len(line) == 0:
            return True
        if line[0] == "#":  # It is a comment
            return True
        return False

    def _parse_shape_map_item_from_line(self, line):
        """
        It is expecting to receive a line which has already been stripped ()
        :param line:
        :return:
        """
        line = self._remove_trailing_comma(line)
        pieces = line.split("@")
        if len(pieces) != 2:
            raise ValueError("There must be exactly a '@' char for each couple selector-label")
        return ShapeMapItem(shape_label=self._label_parser.parse_shape_map_label(pieces[1].strip()),
                            node_selector=self._node_selector_parser.parse_node_selector(pieces[0].strip()))

    @staticmethod
    def _remove_trailing_comma(line):
        if line[-1] == ",":
            return line[:-1]
        return line
