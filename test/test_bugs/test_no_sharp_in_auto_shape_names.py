import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import no_sharp_in_shepe_names
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "no_sharp" + pth.sep  # We just need something with another instantiation property


class TestNoSharpInShapeNames(unittest.TestCase):

    def test_all_classes_no_sharps(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "sharp_chances.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(no_sharp_in_shepe_names(str_result))