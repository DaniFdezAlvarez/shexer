import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "shape_map" + pth.sep

class TestShapeMapFile(unittest.TestCase):

    def test_node(self):
        shape_map_file = _BASE_DIR + "node_selector.sm"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_file=shape_map_file
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "a_node.shex",
                                                      str_target=str_result))

    def test_prefixed_node(self):
        shape_map_file = _BASE_DIR + "prefixed_node_selector.sm"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_file=shape_map_file
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "a_node.shex",
                                                      str_target=str_result))

    def test_focus(self):
        shape_map_file = _BASE_DIR + "focus.sm"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_file=shape_map_file
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "focus_nodes.shex",
                                                      str_target=str_result))

    def test_focus_wildcard(self):
        shape_map_file = _BASE_DIR + "focus_and_wildcard.sm"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_file=shape_map_file
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "focus_and_wildcard.shex",
                                                      str_target=str_result))

    def test_sparql_selector(self):
        shape_map_file = _BASE_DIR + "sparql_selector.sm"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_file=shape_map_file
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "focus_nodes.shex",
                                                      str_target=str_result))

    def test_several_shapemap_items(self):
        shape_map_file = _BASE_DIR + "several_shm_items.sm"
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        shape_map_file=shape_map_file
                        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "several_shm_items.shex",
                                                      str_target=str_result))
