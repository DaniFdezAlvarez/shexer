import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, G1_JSON_LD, G1_NT, G1_TSVO_SPO, G1_XML, G1_N3, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison

from shexer.consts import NT, TSV_SPO, RDF_XML, JSON_LD, N3, TURTLE

_BASE_DIR = BASE_FILES + "general\\"

class TestInputFormat(unittest.TestCase):

    def test_ttl(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_nt(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_NT,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_n3(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_N3,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=N3,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_tsv_spo(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TSVO_SPO,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TSV_SPO,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_xml(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_XML,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=RDF_XML,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_json_ld(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_JSON_LD,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=JSON_LD,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))
