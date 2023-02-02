import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_exact_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "disable_comments" + pth.sep

class TestGraphFileInput(unittest.TestCase):

    def test_disable(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g2.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g2_disable.shex"))

    def test_enable(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g2.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g2_enable.shex"))
