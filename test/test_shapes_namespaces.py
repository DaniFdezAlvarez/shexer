import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE, SHAPES_DEFAULT_NAMESPACE

_BASE_DIR = BASE_FILES + "shapes_namespace" + pth.sep # We just need something with another instantiation property


class TestShapesNamespaces(unittest.TestCase):

    def test_default_namespace(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            shapes_namespace=SHAPES_DEFAULT_NAMESPACE)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_different_namespace(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            shapes_namespace="http://weso.es/DIfferentShapes#")
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "different_namespace.shex",
                                                      str_target=str_result))

    def test_empty_prefix_used(self):
        namespaces = default_namespaces()
        namespaces["http://unuseful.but.yet/here/"] = ""
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=namespaces,
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            shapes_namespace=SHAPES_DEFAULT_NAMESPACE)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "empty_prefix_used.shex",
                                                      str_target=str_result))

    def test_empty_prefix_used_and_no_default(self):
        namespaces = default_namespaces()
        namespaces["http://unuseful.but.yet/here/"] = ""
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=namespaces,
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            shapes_namespace="http://weso.es/DIfferentShapes#")
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "empty_prefix_used_and_no_def.shex",
                                                      str_target=str_result))