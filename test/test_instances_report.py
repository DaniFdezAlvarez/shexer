import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_exact_comparison
import os.path as pth
from shexer.consts import TURTLE, MIXED_INSTANCES, ABSOLUTE_INSTANCES, RATIO_INSTANCES

_BASE_DIR = BASE_FILES + "freq_reports" + pth.sep

class TestGraphFileInput(unittest.TestCase):


    def test_comments_disabled(self):
        """
        Even if a instances report mode is configured, with comments disabled there shouldnt be any
        other content than the pure shape

        :return:
        """
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=True,
                        instances_report_mode=ABSOLUTE_INSTANCES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_comments_disabled.shex"))

    def test_ratio_mode(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False,
                        instances_report_mode=RATIO_INSTANCES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_every_decimal.shex"))

    def test_absolute_mode(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False,
                        instances_report_mode=ABSOLUTE_INSTANCES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_absolute_instances.shex"))

    def test_absolute_mode_unbound_dec(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False,
                        instances_report_mode=MIXED_INSTANCES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_mixed_unbound_dec.shex"))

    def test_absolute_mode_2_dec(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "g_person_infinite_frequencies.ttl",
                        namespaces_dict=default_namespaces(),
                        input_format=TURTLE,
                        disable_comments=False,
                        instances_report_mode=MIXED_INSTANCES,
                        decimals=2)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_exact_comparison(target_str=str_result,
                                                     file_path=_BASE_DIR + "g_person_mixed_2_dec.shex"))
