import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "node_types" + pth.sep

class TestNodeTypes(unittest.TestCase):

    def test_proeprty_to_literal_and_iri(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "property_to_IRI_and_literal.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "property_to_IRI_and_literal.shex",
                                                      str_target=str_result))

