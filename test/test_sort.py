import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE, SHAPES_DEFAULT_NAMESPACE

_BASE_DIR = BASE_FILES + "sort" + pth.sep # We just need something with another instantiation property


class TestSort(unittest.TestCase):

    def test_outgoing_links(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "g_sort.ttl",
            namespaces_dict=default_namespaces(),
            target_classes=["foaf:Person"],
            input_format=TURTLE,
            disable_comments=True,
            shapes_namespace=SHAPES_DEFAULT_NAMESPACE)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g_sort.shex",
                                                      str_target=str_result,
                                                      check_order=True))

    def test_incoming_links(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "g_sort_incoming.ttl",
            namespaces_dict=default_namespaces(),
            target_classes=["foaf:Person"],
            input_format=TURTLE,
            disable_comments=True,
            shapes_namespace=SHAPES_DEFAULT_NAMESPACE,
            inverse_paths=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g_sort_incoming.shex",
                                                      str_target=str_result,
                                                      check_order=True))

    def test_mixed_links(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "g_sort_mixed.ttl",
            namespaces_dict=default_namespaces(),
            target_classes=["foaf:Person"],
            input_format=TURTLE,
            disable_comments=True,
            shapes_namespace=SHAPES_DEFAULT_NAMESPACE,
            inverse_paths=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g_sort_mixed.shex",
                                                      str_target=str_result,
                                                      check_order=True))