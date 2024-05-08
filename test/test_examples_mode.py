import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison, file_vs_str_shex_exact_comparison_excluding_prefixes
from shexer.consts import ALL_EXAMPLES, SHAPE_EXAMPLES, CONSTRAINT_EXAMPLES
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "example_features" + pth.sep



class TestExamplesMode(unittest.TestCase):

    def test_all_classes_examples_disabled(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            examples_mode=None)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "determ_no_examples_no_inverse.shex",
                                                      str_target=str_result))

    def test_all_classes_constraint_examples(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=CONSTRAINT_EXAMPLES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_shex_exact_comparison_excluding_prefixes(file_path=_BASE_DIR + "determ_constraint_examples_no_inverse.shex",
                                                                             str_target=str_result))

    def test_all_classes_constraint_examples_with_inverse(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=CONSTRAINT_EXAMPLES,
            inverse_paths=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_shex_exact_comparison_excluding_prefixes(file_path=_BASE_DIR + "determ_constraint_examples_with_inverse.shex",
                                                                             str_target=str_result))

