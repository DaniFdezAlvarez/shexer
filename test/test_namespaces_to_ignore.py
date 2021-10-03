import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "namespaces_to_ignore" + pth.sep

class TestNamespacesToIgnore(unittest.TestCase):

    def test_excluding_other(self):

        namespaces = {key:value for key, value in default_namespaces().items()}

        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_BASE_DIR + "g1_namespaces.ttl",
                        namespaces_dict=namespaces,
                        namespaces_to_ignore=["http://other.org/"],
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_other_namespace.shex",
                                                      str_target=str_result))

    def test_excluding_direct_other(self):
        namespaces = {key: value for key, value in default_namespaces().items()}

        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_BASE_DIR + "g1_namespaces_indirect.ttl",
                        namespaces_dict=namespaces,
                        namespaces_to_ignore=["http://other.org/"],
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_other_namespace_indirect.shex",
                                                      str_target=str_result))