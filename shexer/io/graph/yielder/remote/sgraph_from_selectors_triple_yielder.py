from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from shexer.consts import RDF_TYPE
from shexer.utils.triple_yielders import tune_token, tune_prop, tune_subj
from shexer.utils.uri import add_corners_if_needed, add_corners_if_it_is_an_uri


class SgraphFromSelectorsTripleYielder(BaseTriplesYielder):

    def __init__(self, shape_map, depth=1, classes_at_last_level=True, instantiation_property=RDF_TYPE,
                 strict_syntax_with_corners=False, allow_untyped_numbers=False, inverse_paths=False):
        super().__init__()
        self._shape_map = shape_map
        self._depth = depth
        self._classes_at_last_level = classes_at_last_level
        self._instantiation_property = instantiation_property
        self._strict_syntax_with_corners = strict_syntax_with_corners
        self._allow_untyped_numbers = allow_untyped_numbers
        self._inverse_paths = inverse_paths


    def yield_triples(self):
        target_nodes = self._collect_every_target_node()
        sgraph = self._shape_map.get_sgraph()
        for a_triple in self._yield_relevant_sgraph_triples(target_nodes, sgraph):
            yield a_triple


    def _collect_every_target_node(self):
        result = set()
        for an_item in self._shape_map.yield_items():
            for a_node in an_item.node_selector.get_target_nodes():
                result.add(a_node)
        return list(result)


    def _yield_relevant_sgraph_triples(self, target_nodes, sgraph):
        for a_triple in self._yield_relevant_direct_triples(target_nodes, sgraph):
            yield a_triple
        if self._inverse_paths:
            for a_triple in self._yield_relevant_inverse_triples(target_nodes, sgraph):
                yield a_triple

    def _yield_relevant_direct_triples(self, target_nodes, sgraph):
        for s, p, o in sgraph.yield_p_o_triples_of_target_nodes(target_nodes=target_nodes,
                                                                depth=self._depth,
                                                                classes_at_last_level=self._classes_at_last_level,
                                                                instantiation_property=self._instantiation_property,
                                                                already_visited=None,
                                                                strict_syntax_with_uri_corners=self._strict_syntax_with_corners):
            yield (tune_subj(a_token=add_corners_if_it_is_an_uri(s)),
                   tune_prop(a_token=add_corners_if_needed(p)),
                   tune_token(a_token=add_corners_if_it_is_an_uri(o),
                              allow_untyped_numbers=self._allow_untyped_numbers)
                   )

    def _yield_relevant_inverse_triples(self, target_nodes, sgraph):
        for s, p, o in sgraph.yield_s_p_triples_of_target_nodes(target_nodes=target_nodes,
                                                                depth=self._depth,
                                                                classes_at_last_level=self._classes_at_last_level,
                                                                instantiation_property=self._instantiation_property,
                                                                already_visited=None,
                                                                strict_syntax_with_uri_corners=self._strict_syntax_with_corners):
            yield (tune_subj(a_token=add_corners_if_it_is_an_uri(s)),
                   tune_prop(a_token=add_corners_if_needed(p)),
                   tune_token(a_token=add_corners_if_it_is_an_uri(o),
                              allow_untyped_numbers=self._allow_untyped_numbers)
                   )








