import unittest
from shexer.shaper import Shaper
from shexer.consts import NT
from test.const import G1_NT, BASE_FILES, BASE_FILES_GENERAL, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

_BASE_DIR = BASE_FILES + "instances_file_input" + pth.sep

class TestInstancesFileInput(unittest.TestCase):

    def test_all_classes_all_instances(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_NT,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True,
                        instances_file_input=_BASE_DIR + "g1_all_instances.nt")
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_all_classes_some_instances(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_NT,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True,
                        instances_file_input=_BASE_DIR + "g1_some_instances.nt")
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "all_classes_some_instances.shex",
                                                      str_target=str_result))

    def test_some_classes_some_instances(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person"],
                        graph_file_input=G1_NT,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True,
                        instances_file_input=_BASE_DIR + "g1_some_instances.nt")
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "some_classes_some_instances.shex",
                                                      str_target=str_result))

    def test_some_classes_all_instances(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person"],
                        graph_file_input=G1_NT,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True,
                        instances_file_input=_BASE_DIR + "g1_all_instances.nt")
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "some_classes_all_instances.shex",
                                                      str_target=str_result))