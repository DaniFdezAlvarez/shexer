import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import NT

_BASE_DIR = BASE_FILES + "untyped_numbers" + pth.sep

class TestInferNumericTypesForUntypedLiterals(unittest.TestCase):

    def test_untyped_int(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_BASE_DIR + "g1_untyped_age.nt",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        infer_numeric_types_for_untyped_literals=True,
                        input_format=NT,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_untyped_int_and_float(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=_BASE_DIR + "g1_untyped_age.nt",  # TODO CHANGE THIS AND MORE
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        infer_numeric_types_for_untyped_literals=True,
                        input_format=NT,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))