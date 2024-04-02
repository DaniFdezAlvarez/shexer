


from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder


class MultiZipTriplesYielder(BaseTriplesYielder):

    def __init__(self, multiyielders):
        super().__init__()
        self._multiyielders = multiyielders

        self._triples_yielded_from_used_yielders = 0
        self._error_triples_from_used_yielders = 0
        self._last_yielder = None

        self._current_yielder = None

    def yield_triples(self, parse_namespaces=True):
        self._reset_count()
        for a_yielder in self._multiyielders:
            self._current_yielder = a_yielder
            for a_triple in a_yielder.yield_triples():
                yield a_triple
            self._triples_yielded_from_used_yielders += a_yielder.yielded_triples
            self._error_triples_from_used_yielders += a_yielder.error_triples

    @property
    def yielded_triples(self):
        triples_current_yielder = 0 if self._current_yielder is None else self._current_yielder.yielded_triples
        return self._triples_yielded_from_used_yielders + triples_current_yielder

    @property
    def error_triples(self):
        errors_current_yielder = 0 if self._current_yielder is None else self._current_yielder.error_triples
        return self._error_triples_from_used_yielders + errors_current_yielder

    def _reset_count(self):
        self._error_triples_from_used_yielders = 0
        self._triples_yielded_from_used_yielders = 0
