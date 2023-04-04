from shexer.io.sparql.query import \
    query_endpoint_po_of_an_s, \
    query_endpoint_single_variable, \
    query_endpoint_sp_of_an_o
from shexer.model.graph.abstract_sgraph import SGraph
from shexer.model.graph.rdflib_sgraph import RdflibSgraph
from shexer.utils.uri import remove_corners
from rdflib import Graph
from shexer.consts import RDF_TYPE

_DEF_SUBJ_VARIABLE = "?s"
_DEF_SUBJ_ID = "s"

_DEF_PRED_VARIABLE = "?p"
_DEF_PRED_ID = "p"

_DEF_OBJ_VARIABLE = "?o"
_DEF_OBJ_ID = "o"

class EndpointSGraph(SGraph):

    def __init__(self, endpoint_url, store_locally=True):
        super().__init__()
        self._endpoint_url = endpoint_url
        self._store_locally = store_locally
        self._local_sgraph = RdflibSgraph(rdflib_graph=Graph()) if store_locally else None
        self._subjects_tracked = set() if store_locally else None
        self._objects_tracked = set() if store_locally else None



    def query_single_variable(self, str_query, variable_id):
        return query_endpoint_single_variable(variable_id=variable_id,
                                              str_query=str_query,
                                              endpoint_url=self._endpoint_url)

    def serialize_current_local_sgraph(self, path_file, format):
        if self._local_sgraph is not None:
            self._local_sgraph.serialize(path=path_file,
                                         format=format)


    def yield_class_triples_of_an_s(self, target_node, instantiation_property):
        if not self._store_locally:
            for a_triple in self._yield_remote_class_triples_of_an_s(target_node, instantiation_property):
                yield a_triple
        else:
            for a_triple in self._yield_local_class_triples_of_an_s(target_node, instantiation_property):
                yield a_triple

    def yield_classes_with_instances(self, instantiation_property=RDF_TYPE):
        str_query = "SELECT distinct {0} where {{ {1} <{2}> {0} . }}".format(_DEF_OBJ_VARIABLE,
                                                                             _DEF_SUBJ_VARIABLE,
                                                                              remove_corners(
                                                                                  a_uri=instantiation_property,
                                                                                  raise_error_if_no_corners=False)
                                                                              )
        for an_elem in query_endpoint_single_variable(endpoint_url=self._endpoint_url,
                                                      str_query=str_query,
                                                      variable_id=_DEF_OBJ_ID):
            yield str(an_elem)


    def _yield_remote_class_triples_of_an_s(self, target_node, instantiation_property):
        str_query = "SELECT {0} WHERE {{ <{1}> <{2}> {0} . }}".format(_DEF_OBJ_VARIABLE,
                                                                      remove_corners(a_uri=target_node,
                                                                                     raise_error_if_no_corners=False),
                                                                      remove_corners(a_uri=instantiation_property,
                                                                                     raise_error_if_no_corners=False))
        for an_elem in query_endpoint_single_variable(endpoint_url=self._endpoint_url,
                                                      str_query=str_query,
                                                      variable_id=_DEF_OBJ_ID):
            yield ("<" + target_node + ">", "<" + instantiation_property + ">", an_elem)


    def _yield_local_class_triples_of_an_s(self, target_node, instantiation_property):
        if target_node not in self._subjects_tracked:
            for a_triple in self._yield_remote_class_triples_of_an_s(target_node, instantiation_property):
                self._store_triple_locally(a_triple)
            self._subjects_tracked.add(target_node)
        for a_triple in self._local_sgraph.yield_class_triples_of_an_s(target_node, instantiation_property):
            yield a_triple


    def yield_p_o_triples_of_an_s(self, target_node):
        if not self._store_locally:
            for a_triple in self._yield_remote_p_o_triples_of_an_s(target_node):
                yield a_triple
        else:
            for a_triple in self._yield_local_p_o_triples_of_an_s(target_node):
                yield a_triple

    def yield_s_p_triples_of_an_o(self, target_node):
        if not self._store_locally:
            for a_triple in self._yield_remote_s_p_triples_of_an_o(target_node):
                yield a_triple
        else:
            for a_triple in self._yield_local_s_p_triples_of_an_o(target_node):
                yield a_triple


    def _yield_remote_p_o_triples_of_an_s(self, target_node):
        str_query = "SELECT {0} {1} WHERE {{ <{2}> {0} {1} .}} ".format(_DEF_PRED_VARIABLE,
                                                                        _DEF_OBJ_VARIABLE,
                                                                        remove_corners(a_uri=target_node,
                                                                                       raise_error_if_no_corners=False))
        for a_tuple_po in query_endpoint_po_of_an_s(endpoint_url=self._endpoint_url,
                                                    str_query=str_query,
                                                    p_id=_DEF_PRED_ID,
                                                    o_id=_DEF_OBJ_ID):
            yield "<" + target_node + ">", a_tuple_po[0], a_tuple_po[1]

    def _yield_remote_s_p_triples_of_an_o(self, target_node):
        str_query = "SELECT {0} {1} WHERE {{ {0} {1} <{2}> .}}".format(_DEF_SUBJ_VARIABLE,
                                                                       _DEF_PRED_VARIABLE,
                                                                       remove_corners(a_uri=target_node,
                                                                                      raise_error_if_no_corners=False))
        for a_tuple_sp in query_endpoint_sp_of_an_o(endpoint_url=self._endpoint_url,
                                                    str_query=str_query,
                                                    p_id=_DEF_PRED_ID,
                                                    s_id=_DEF_SUBJ_ID):
            yield a_tuple_sp[0], a_tuple_sp[1], "<" + target_node + ">"


    def _yield_local_p_o_triples_of_an_s(self, target_node):
        if target_node not in self._subjects_tracked:
            for a_triple in self._yield_remote_p_o_triples_of_an_s(target_node):
                self._store_triple_locally(a_triple)
            self._subjects_tracked.add(target_node)
        for a_triple in self._local_sgraph.yield_p_o_triples_of_an_s(target_node):
            yield a_triple

    def _yield_local_s_p_triples_of_an_o(self, target_node):
        if target_node not in self._objects_tracked:
            for a_triple in self._yield_remote_s_p_triples_of_an_o(target_node):
                self._store_triple_locally(a_triple)
            self._objects_tracked.add(target_node)
        for a_triple in self._local_sgraph.yield_s_p_triples_of_an_o(target_node):
            yield a_triple

    def _store_triple_locally(self, a_triple):
        self._local_sgraph.add_triple(a_triple)