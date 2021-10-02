import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import NT, TURTLE

_BASE_DIR = BASE_FILES + "general" + pth.sep

class TestUrlGraphFormat(unittest.TestCase):

    def test_ttl(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        url_graph_input="https://raw.githubusercontent.com/DaniFdezAlvarez/shexerp3/develop/test/t_files/t_graph_1.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))


    def test_nt(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        url_graph_input="https://raw.githubusercontent.com/DaniFdezAlvarez/shexerp3/develop/test/t_files/t_graph_1.nt",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))


