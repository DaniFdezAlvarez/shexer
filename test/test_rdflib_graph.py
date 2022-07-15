import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from rdflib import Graph

from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "general" + pth.sep

class TestGraphFileInput(unittest.TestCase):

    def test_parsing_file(self):
        a_g = Graph()
        a_g.parse(G1, format="turtle")

        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        rdflib_graph=a_g,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_all_classes_mode(self):
        a_g = Graph()
        a_g.parse(G1, format="turtle")

        shaper = Shaper(all_classes_mode=True,
                        rdflib_graph=a_g,
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

