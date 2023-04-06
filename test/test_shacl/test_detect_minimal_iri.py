import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison, graph_comparison_file_vs_str
import os.path as pth

from shexer.consts import TURTLE, SHACL_TURTLE



_BASE_DIR = BASE_FILES + "min_iri" + pth.sep  # We just need something with another instantiation property


class TestDetectMinimalIri(unittest.TestCase):

    def test_all_classes_g1_enabled(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "shacl_g1_all_classes_no_comments_min_iri.ttl",
                                                     str_target=str_result))

    def test_g1_different_namespaces_per_class(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR+"g1_different_namespaces_per_class.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "shacl_g1_different_namespaces_per_class.ttl",
                                                     str_target=str_result))


    def test_g1_different_namespaces_per_instance(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR+"g1_different_namespaces_per_instance.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "shacl_g1_different_namespaces_per_instance.ttl",
                                                     str_target=str_result))

    def test_g1_different_base_per_instance_no_sep_char(self):
        """
        :Person should be [http://example.org/ns1/], not [http://example.org/ns1/aa]
        :return:
        """
        shaper = Shaper(
            graph_file_input=_BASE_DIR+"g1_different_base_per_instance_no_sep_char.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "shacl_g1_different_namespaces_per_class.ttl",
                                                     str_target=str_result))

