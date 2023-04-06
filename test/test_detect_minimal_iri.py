import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE, SHACL_TURTLE



_BASE_DIR = BASE_FILES + "instantiation_prop" + pth.sep  # We just need something with another instantiation property


class TestDetectMinimalIri(unittest.TestCase):

    def test_all_classes_g1(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        print(str_result)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))



