import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, G1_ALL_CLASSES_NO_COMMENTS, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "threshold" + pth.sep

class TestGraphFileInput(unittest.TestCase):

    def test_t_0(self):
        shaper = Shaper(graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True,
                                       acceptance_threshold=0)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))
    def test_t_1(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True,
                                       acceptance_threshold=1)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_t1.shex",
                                                      str_target=str_result))

    def test_t_05(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True,
                                       acceptance_threshold=.5)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_t05.shex",
                                                      str_target=str_result))

    def test_t_051(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True,
                                       acceptance_threshold=.51)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_t051.shex",
                                                      str_target=str_result))
