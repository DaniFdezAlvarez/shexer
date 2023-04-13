import unittest
from shexer.shaper import Shaper
from test.const import G1_NT, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "no_slash_prefixed" + pth.sep  # We just need something with another instantiation property


class TestNoSharpNorSlashDueToPrefixing(unittest.TestCase):

    def test_shorter_prefixes_g1(self):
        shaper = Shaper(
            graph_file_input=G1_NT,
            namespaces_dict={"http://example.org/": "ex",
            "http://www.w3.org/XML/1998/": "xml",
            "http://www.w3.org/1999/02/": "rdf",
            "http://www.w3.org/2000/01#": "rdfs",
            "http://www.w3.org/2001#": "xsd",
            "http://xmlns.com/foaf/": "foaf"
            },
            all_classes_mode=True,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_no_prefix_except_shapes.shex",
                                                      str_target=str_result))