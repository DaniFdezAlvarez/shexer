import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "opt_cardinality" + pth.sep  # We just need something with another instantiation property


class TestAllowOptCardinality(unittest.TestCase):

    def test_opt_enabled(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "g4_opt_cardinality.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            allow_opt_cardinality=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g4_opt_enabled.shex",
                                                      str_target=str_result))

    def test_opt_disabled(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "g4_opt_cardinality.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            allow_opt_cardinality=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g4_opt_disabled.shex",
                                                      str_target=str_result))