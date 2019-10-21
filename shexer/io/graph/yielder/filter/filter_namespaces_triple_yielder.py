from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from shexer.utils.triple_yielders import check_if_property_belongs_to_namespace_list

class FilterNamespacesTriplesYielder(BaseTriplesYielder):

    def __init__(self, actual_triple_yielder, namespaces_to_ignore):
        super().__init__()
        self._actual_triple_yielder = actual_triple_yielder
        self._namespaces_to_ignore = namespaces_to_ignore


    def yield_triples(self):
        for a_triple in self._actual_triple_yielder.yield_triples():
            if self._pass_filters(a_triple):
                yield a_triple

    def _pass_filters(self, a_triple):
        return not check_if_property_belongs_to_namespace_list(str_prop=str(a_triple[1]),
                                                               namespaces=self._namespaces_to_ignore)
