from rdflib.graph import Graph, URIRef, Literal, BNode
from dbshx.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from dbshx.consts import N3, TURTLE, RDF_XML

from dbshx.model.Literal import Literal as model_Literal
from dbshx.model.IRI import IRI as model_IRI
from dbshx.model.bnode import BNode as model_BNode
from dbshx.model.property import Property as model_Property

from dbshx.utils.uri import decide_literal_type

_SUPPORTED_FORMATS = [N3, TURTLE, RDF_XML]

_XML_WRONG_URI = "http://www.w3.org/XML/1998/namespace"

class RdflibTripleYielder(BaseTriplesYielder):

    def __init__(self, input_format=TURTLE, source_file=None, namespaces_to_ignore=None, allow_untyped_numbers=False,
                 raw_graph=None, namespaces_dict=None):
        super(RdflibTripleYielder, self).__init__()
        self._check_input_format(input_format)

        self._input_format = input_format
        self._source_file = source_file
        self._namespaces_to_ignore = namespaces_to_ignore
        self._allow_untyped_numbers = allow_untyped_numbers
        self._raw_graph = raw_graph
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
                                              # This object can be modified (and will be consumed externaly)
                                              # when parse_namespaces in yiled_triples() is set to True

        self._triples_count = 0

        self._prefixes_parsed = False


    def yield_triples(self, parse_namespaces=True):
        self._reset_count()
        tmp_graph = self._get_tmp_graph()
        if parse_namespaces:
            self._integrate_namespaces_from_parsed_graph(tmp_graph, self._namespaces_dict)
            self._prefixes_parsed = True
        for sub,pred,obj in tmp_graph:
            yield (
                self._turn_rdflib_token_into_model_obj(sub),
                self._turn_rdflib_prop_into_model_obj(pred),
                self._turn_rdflib_token_into_model_obj(obj)
            )
            self._triples_count += 1



    def _turn_rdflib_token_into_model_obj(self, rdflib_obj):
        if type(rdflib_obj) == URIRef:
            return model_IRI(str(rdflib_obj))
        elif type(rdflib_obj) == Literal:
            return self._turn_into_model_literal(rdflib_obj)
        elif type(rdflib_obj) == BNode:
            return model_BNode(identifier=str(rdflib_obj))
        else:
            raise ValueError("Not recognized type of rdflib element: " + type(rdflib_obj) + " ( " + str(rdflib_obj) + " )")

    def _turn_rdflib_prop_into_model_obj(self, rdflib_obj):
        if type(rdflib_obj) == URIRef:
            return model_Property(str(rdflib_obj))
        else:
            raise ValueError("Trying to convert into a model property en element which is not "
                             "supposed to be a property: " + type(rdflib_obj) + " ( " + str(rdflib_obj) + " )")

    def _get_tmp_graph(self):
        result = Graph()
        if self._source_file is not None:
            result.parse(source=self._source_file, format=self._input_format)
        else:
            result.parse(data=self._raw_graph, format=self._input_format)
        return result

    @staticmethod
    def _integrate_namespaces_from_parsed_graph(a_graph, namespaces_dict):

        for a_prefix_namespace_tuple in a_graph.namespaces():
            candidate_uri = str(a_prefix_namespace_tuple[1])
            if candidate_uri not in namespaces_dict:
                if candidate_uri == _XML_WRONG_URI:  # XML fix...
                    candidate_uri += "/"             # XML fix...
                namespaces_dict[candidate_uri] = str(a_prefix_namespace_tuple[0])
            # There is no else here. In case of conflict between the parsed content and the dict provided by the user,
            # the user's one have priority


    @staticmethod
    def _turn_into_model_literal(rdflib_literal):
        content = str(rdflib_literal)
        return model_Literal(content=content,
                             elem_type=decide_literal_type(content))

    @staticmethod
    def _check_input_format(input_format):
        if input_format not in _SUPPORTED_FORMATS:
            raise ValueError("Unsupported input format: " + input_format)

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return 0  # With rdflib, a single error will cause to fail the parsing process


    @property
    def namespaces(self):
        if not self._prefixes_parsed:
            tmp_graph = self._get_tmp_graph()
            self._integrate_namespaces_from_parsed_graph(tmp_graph, self._namespaces_dict)
            self._prefixes_parsed = True
        return self._namespaces_dict


    def _reset_count(self):
        self._triples_count = 0




