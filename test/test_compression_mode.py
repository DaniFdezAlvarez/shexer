import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE_ITER, GZ



_BASE_DIR = BASE_FILES + "compression" + pth.sep


class TestCompressionMode(unittest.TestCase):

    def test_ttl_iter_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.ttl.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        print(str_result)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))