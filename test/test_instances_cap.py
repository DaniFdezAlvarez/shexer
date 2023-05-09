import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE_ITER


_BASE_DIR = BASE_FILES + "instances_cap" + pth.sep


class TestInstancesCap(unittest.TestCase):
    """
    We must use a deterministic input format, such as NT or TURTLE_ITER (something non rdflib-based)
    to test this. Otherwhise, the instance(s) chosen for each test could be different in different
    executions of the tests

    """

    def test_no_cap_all_g1(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            instances_cap=-1)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_cap_1_all_g1(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            instances_cap=1)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "all_classes_cap_1.shex",
                                                      str_target=str_result))

    def test_cap_3_all_g1(self):  # exceeds one class limit (of instances), doest reach the other class limit
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            instances_cap=3)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "all_classes_cap_3.shex",
                                                      str_target=str_result))

    def test_cap_5_all_g1(self):  # exceeds every class limit (of instances), doest reach the other class limit
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            instances_cap=5)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_cap_1_one_target_g1(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=False,
            target_classes=["foaf:Person"],
            input_format=TURTLE_ITER,
            disable_comments=True,
            instances_cap=1)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "target_person_cap_1.shex",
                                                      str_target=str_result))


    def test_cap_5_one_target_g1(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=False,
            target_classes=["foaf:Person"],
            input_format=TURTLE_ITER,
            disable_comments=True,
            instances_cap=5)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "target_person_cap_5.shex",
                                                      str_target=str_result))

    def test_cap_1_all_targets_g1(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=False,
            target_classes=["foaf:Person", "foaf:Document"],
            input_format=TURTLE_ITER,
            disable_comments=True,
            instances_cap=1)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "all_classes_cap_1.shex",
                                                      str_target=str_result))



