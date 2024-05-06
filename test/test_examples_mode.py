import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
from shexer.consts import ALL_EXAMPLES, SHAPE_EXAMPLES, CONSTRAINT_EXAMPLES
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "instantiation_prop" + pth.sep  # We just need something with another instantiation property



class TestExamplesMode(unittest.TestCase):

    def test_all_classes_g1_examples_disabled(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            examples_mode=None)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_all_classes_g1_all_examples(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            examples_mode=ALL_EXAMPLES)
        str_result = shaper.shex_graph(string_output=True)
        print(str_result)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

