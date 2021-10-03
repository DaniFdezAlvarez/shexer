import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "keep_less_specific" + pth.sep
_G1_SEV_NAMES = _BASE_DIR + "g1_several_names.ttl"

class TestKeepLessSpecific(unittest.TestCase):

    def test_keep_less_no_compliant(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_G1_SEV_NAMES,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        all_instances_are_compliant_mode=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "keep_less_no_compliant.shex",
                                                      str_target=str_result))

    def test_no_keep_less_no_compliant(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_G1_SEV_NAMES,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        all_instances_are_compliant_mode=False,
                        keep_less_specific=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "no_keep_less_no_compliant.shex",
                                                      str_target=str_result))

    def test_keep_less_compliant(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_G1_SEV_NAMES,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        all_instances_are_compliant_mode=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "keep_less_compliant.shex",
                                                      str_target=str_result))

    def test_no_keep_less_compliant(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_G1_SEV_NAMES,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True,
                        all_instances_are_compliant_mode=True,
                        keep_less_specific=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "no_keep_less_compliant.shex",
                                                      str_target=str_result))

