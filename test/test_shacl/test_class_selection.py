import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces
from test.t_utils import graph_comparison_file_vs_str
import os.path as pth
from shexer.consts import TURTLE, SHACL_TURTLE

_BASE_DIR = BASE_FILES + "shacl" + pth.sep


class TestClassSelection(unittest.TestCase):

    def test_all_classes_mode(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "g1_all_classes.ttl",
                                                     str_target=str_result))

    def test_all_classes_with_target_classes(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=False,
            target_classes=["http://xmlns.com/foaf/0.1/Person",
                            "http://xmlns.com/foaf/0.1/Document"],
            input_format=TURTLE,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "g1_all_classes.ttl",
                                                     str_target=str_result))

    def test_some_classes_with_target_classes(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=False,
            target_classes=["http://xmlns.com/foaf/0.1/Person"],
            input_format=TURTLE,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "g1_person.ttl",
                                                     str_target=str_result))
