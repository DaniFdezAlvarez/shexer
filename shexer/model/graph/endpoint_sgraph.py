from shexer.io.sparql.query import query_endpoint_po_of_an_s, query_endpoint_single_variable
from shexer.model.graph.abstract_sgraph import SGraph

_DEF_PRED_VARIABLE = "?p"
_DEF_PRED_ID = "p"

_DEF_OBJ_VARIABLE = "?o"
_DEF_OBJ_ID = "o"

class EndpointSGraph(SGraph):

    def __init__(self, endpoint_url):
        super().__init__()
        self._endpoint_url = endpoint_url

    def query_single_variable(self, str_query, variable_id):
        return query_endpoint_single_variable(variable_id=variable_id,
                                              str_query=str_query,
                                              endpoint_url=self._endpoint_url)


    def yield_class_triples_of_an_s(self, target_node, instantiation_property):
        str_query = "SELECT {0} WHERE {{ <{1}> <{2}> {0} . }}".format(_DEF_OBJ_VARIABLE, target_node, instantiation_property)
        for an_elem in query_endpoint_single_variable(endpoint_url=self._endpoint_url,
                                                      str_query=str_query,
                                                      variable_id=_DEF_OBJ_ID):
            yield (target_node, instantiation_property, an_elem)


    def yield_p_o_triples_of_an_s(self, target_node):
        str_query = "SELECT {0} {1} WHERE {{ <{2}> {0} {1} .}} ".format(_DEF_PRED_VARIABLE, _DEF_OBJ_VARIABLE, target_node)
        for a_tuple_po in query_endpoint_po_of_an_s(endpoint_url=self._endpoint_url,
                                                    str_query=str_query,
                                                    p_id=_DEF_PRED_ID,
                                                    o_id=_DEF_OBJ_ID):

            yield target_node, a_tuple_po[0], a_tuple_po[1]
