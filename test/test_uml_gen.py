import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import check_file_exist, delete_file,file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "uml" + pth.sep
_A_PATH_FOR_IMG = _BASE_DIR + "any_path.png"


class TestUmlGen(unittest.TestCase):

    def test_base_gen(self):
        delete_file(_A_PATH_FOR_IMG)  # pre-condition
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True)
        shaper.shex_graph(to_uml_path=_A_PATH_FOR_IMG)
        try:
            check_file_exist(_A_PATH_FOR_IMG)
        finally:
            delete_file(_A_PATH_FOR_IMG)

    def test_gen_uml_and_classical_output(self):
        def test_base_gen(self):
            delete_file(_A_PATH_FOR_IMG)  # pre-condition
            shaper = Shaper(
                graph_file_input=G1,
                namespaces_dict=default_namespaces(),
                all_classes_mode=True,
                input_format=TURTLE,
                disable_comments=True)
            str_result = shaper.shex_graph(to_uml_path=_A_PATH_FOR_IMG)
            self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                          str_target=str_result))
            try:
                check_file_exist(_A_PATH_FOR_IMG)
            finally:
                delete_file(_A_PATH_FOR_IMG)

    def test_or_enabled_choice_useful_IRI(self):
        shaper = Shaper(graph_file_input=BASE_FILES + "disable_or" + pth.sep + "g_or_example_expandable_IRI.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True,
                        disable_or_statements=False)
        str_result = shaper.shex_graph(string_output=True, to_uml_path="here.png")
        # In case the choice includes the IRI macro, then no OR should appear
        print(str_result)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES + "disable_or" + pth.sep + "or_enabled.shex",
                                                      str_target=str_result,
                                                      or_shapes=True))
