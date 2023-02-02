import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_exact_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "freq_reports" + pth.sep

class TestGraphFileInput(unittest.TestCase):


    def test_decimals_no_round(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False,
                        decimals=-1)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_every_decimal.shex"))

    def test_decimals_round_two(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False,
                        decimals=2)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_2_decimals.shex"))

    def test_no_decimals(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False,
                        decimals=0)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_0_decimals.shex"))
