from rdflib import URIRef, Graph, Literal, BNode
from shexer.model.graph.abstract_sgraph import SGraph
from shexer.utils.triple_yielders import tune_token, tune_prop, tune_subj
from shexer.utils.uri import add_corners_if_it_is_an_uri, remove_corners
from shexer.core.instances.pconsts import _S, _P, _O
from shexer.model.IRI import IRI as ModelIRI
from shexer.model.property import Property as ModelProperty
from shexer.model.Literal import Literal as ModelLiteral
from shexer.model.bnode import BNode as ModelBnode
from shexer.consts import RDF_TYPE



class RdflibSgraph(SGraph):

    def __init__(self, rdflib_graph=None, source_file=None, raw_graph=None, format="turtle"):
        """
        Pass an rdflib.Graph object or the params source_file and format to parse a local rdf

        :param rdflib_graph:
        :param source_file:
        :param format:
        """
        super().__init__()
        self._rdflib_graph = rdflib_graph if rdflib_graph is not None else self._build_rdflib_graph(source=source_file,
                                                                                                    raw_graph=raw_graph,
                                                                                                    format=format)

    def query_single_variable(self, str_query, variable_id):
        rows_res = self._rdflib_graph.query(str_query)
        return [str(a_row[0]) for a_row in rows_res]

    def serialize(self, path, format):
        self._rdflib_graph.serialize(destination=path,
                                     format=format)

    def yield_p_o_triples_of_an_s(self, target_node):
        for s, p ,o in self._rdflib_graph.triples((URIRef(remove_corners(a_uri=target_node,
                                                                         raise_error_if_no_corners=False)),
                                                   None,
                                                   None)):
            yield self._add_URI_corners_if_needed(s),\
                  self._add_URI_corners_if_needed(p),\
                  self._add_URI_corners_if_needed(self._add_lang_if_needed(o))

    def yield_s_p_triples_of_an_o(self, target_node):
        for s, p, o in self._rdflib_graph.triples((None,
                                                   None,
                                                   URIRef(remove_corners(a_uri=target_node,
                                                                         raise_error_if_no_corners=False)))):
            yield self._add_URI_corners_if_needed(s),\
                  self._add_URI_corners_if_needed(p),\
                  self._add_URI_corners_if_needed(o)


    def yield_class_triples_of_an_s(self, target_node, instantiation_property):
        for s ,p, o in self._rdflib_graph.triples((URIRef(remove_corners(a_uri=target_node,
                                                                         raise_error_if_no_corners=False)),
                                                   URIRef(remove_corners(a_uri=instantiation_property,
                                                                         raise_error_if_no_corners=False)),
                                                   None)):
            yield self._add_URI_corners_if_needed(s),\
                  self._add_URI_corners_if_needed(p),\
                  self._add_URI_corners_if_needed(self._add_lang_if_needed(o))

    def add_triple(self, a_triple):
        """
        It receives a tuple of 3 string elements. It adds it to the local rdflib graph
        :param a_triple:
        :return:
        """

        subj = tune_subj(add_corners_if_it_is_an_uri(a_triple[_S]),
                         raise_error_if_no_corners=False)
        prop = tune_prop(add_corners_if_it_is_an_uri(a_triple[_P]),
                         raise_error_if_no_corners=False)
        obj = tune_token(add_corners_if_it_is_an_uri(a_triple[_O]),
                         raise_error_if_no_corners=False)

        self._rdflib_graph.add((self._turn_obj_into_rdflib_element(subj),
                                self._turn_obj_into_rdflib_element(prop),
                                self._turn_obj_into_rdflib_element(obj)))

    def yield_classes_with_instances(self, instantiation_property=RDF_TYPE):
        result = set()
        for s ,_, _ in self._rdflib_graph.triples((None,
                                                   URIRef(remove_corners(a_uri=instantiation_property,
                                                                         raise_error_if_no_corners=False)),
                                                   None)):
            result.add(str(s))
        for elem in result:
            yield elem


    def _turn_obj_into_rdflib_element(self, model_elem):
        if type(model_elem) == ModelIRI or type(model_elem) == ModelProperty:
            return URIRef(model_elem.iri)
        elif type(model_elem) == ModelLiteral:
            return Literal(lexical_or_value=str(model_elem),
                           datatype=model_elem.elem_type)
        elif type(model_elem) == ModelBnode:
            return BNode(value=str(model_elem))
        else:
            raise ValueError("Unexpected type of element. " + str(model_elem) + ": " + str(type(model_elem)))


    def _build_rdflib_graph(self, source, raw_graph, format):
        result = Graph()
        if source is not None:
            result.parse(source=source, format=format)
        else:
            result.parse(data=raw_graph, format=format)
        return result

    def _add_lang_if_needed(self, rdflib_obj):
        """
        It returns a string representation with lang if it is a langString
        :param rdflib_obj:
        :return:
        """
        if type(rdflib_obj) == Literal and rdflib_obj.language is not None:
           return '"' + str(rdflib_obj) + '"@' + rdflib_obj.language
        return rdflib_obj

    def _add_URI_corners_if_needed(self, rdflib_obj):
        if type(rdflib_obj) == URIRef:
            return "<"+ str(rdflib_obj) + ">"
        return str(rdflib_obj)