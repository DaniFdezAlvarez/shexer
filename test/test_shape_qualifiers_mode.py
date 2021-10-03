import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES
from test.t_utils import file_vs_str_tunned_comparison
from shexer.consts import TURTLE
import os.path as pth

_BASE_DIR = BASE_FILES + "qualifiers" + pth.sep

class TestShapeQualifiersMode(unittest.TestCase):

    def test_wikidata_virus_and_qualifiers(self):
        shape_map_raw = "SPARQL'SELECT DISTINCT ?virus WHERE {   VALUES ?virus {  wd:Q82069695  }  }'@<Virus>  "
        # wd:Q8351095  wd:Q16983356 wd:Q4902157  wd:Q278567 wd:Q16983360 wd:Q16991954

        namespaces_dict = {
            "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
            "http://www.wikidata.org/prop/": "p",
            "http://www.wikidata.org/prop/direct/": "wdt",
            "http://www.wikidata.org/entity/": "wd",
            "http://www.w3.org/2001/XMLSchema#": "xsd",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
            "http://www.w3.org/XML/1998/namespace": "xml",
            "http://wikiba.se/ontology#": "wikibase",
            "http://schema.org/": "schema",
            "http://www.w3.org/2004/02/skos/core#": "skos"
        }

        shaper = Shaper(shape_map_raw=shape_map_raw,
                        graph_file_input=_BASE_DIR + "virus_wikidata_depth2.ttl",
                        input_format=TURTLE,
                        all_instances_are_compliant_mode=True,
                        infer_numeric_types_for_untyped_literals=True,
                        discard_useless_constraints_with_positive_closure=True,
                        keep_less_specific=True,
                        instantiation_property="http://www.wikidata.org/prop/direct/P31",
                        namespaces_dict=namespaces_dict,
                        namespaces_for_qualifier_props=["http://www.wikidata.org/prop/"],
                        shape_qualifiers_mode=True,
                        disable_comments=True,
                        all_classes_mode=False,
                        allow_opt_cardinality=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "virus_qualifiers.shex",
                                                      str_target=str_result))
