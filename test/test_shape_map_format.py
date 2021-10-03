import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces
from shexer.consts import JSON, FIXED_SHAPE_MAP
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "shape_map" + pth.sep

class TestShapeMapFormat(unittest.TestCase):



    def test_some_fixed_shape_map(self):
        shape_map = "<http://example.org/Jimmy>@<Person>"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_raw=shape_map,
                        shape_map_format=FIXED_SHAPE_MAP
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "a_node.shex",
                                                      str_target=str_result))

    def test_json_node(self):
        # shape_map = "<http://example.org/Jimmy>@<Person>"
        shape_map = '[{"nodeSelector" : "<http://example.org/Jimmy>", "shapeLabel": "<Person>"}]'
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_raw=shape_map,
                        shape_map_format=JSON
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "a_node.shex",
                                                      str_target=str_result))

    def test_json_prefixed_node(self):
        shape_map = '[{"nodeSelector" : "ex:Jimmy", "shapeLabel": "<Person>"}]'
        # shape_map = "ex:Jimmy@<Person>"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_raw=shape_map,
                        shape_map_format=JSON
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "a_node.shex",
                                                      str_target=str_result))

    def test_json_focus(self):
        shape_map = '[{"nodeSelector" : "{FOCUS a foaf:Person}", "shapeLabel": "<Person>"}]'
        # shape_map = "{FOCUS a foaf:Person}@<Person>"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_raw=shape_map,
                        shape_map_format=JSON
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "focus_nodes.shex",
                                                      str_target=str_result))

    def test_json_focus_wildcard(self):
        shape_map = '[{"nodeSelector" : "{FOCUS foaf:name _}", "shapeLabel": "<WithName>"}]'
        # shape_map = "{FOCUS foaf:name _}@<WithName>"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_raw=shape_map,
                        shape_map_format=JSON
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "focus_and_wildcard.shex",
                                                      str_target=str_result))

    def test_json_sparql_selector(self):
        shape_map = '[{"nodeSelector" : "SPARQL \'select ?p where { ?p a foaf:Person }\'", "shapeLabel": "<Person>"}]'
        # shape_map = "SPARQL \"select ?p where { ?p a foaf:Person }\"@<Person>"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_raw=shape_map,
                        shape_map_format=JSON
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "focus_nodes.shex",
                                                      str_target=str_result))

    def test_json_several_shapemap_items(self):
        shape_map = '[{"nodeSelector" : "{FOCUS a foaf:Person}", "shapeLabel": "<Person>"},' \
                    '{"nodeSelector" : "{FOCUS a foaf:Document}", "shapeLabel": "<Document>"}]'
        # shape_map = "{FOCUS a foaf:Person}@<Person>\n{FOCUS a foaf:Document}@<Document>"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_raw=shape_map,
                        shape_map_format=JSON
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "several_shm_items.shex",
                                                      str_target=str_result))