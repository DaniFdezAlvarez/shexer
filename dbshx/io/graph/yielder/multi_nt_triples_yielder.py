from dbshx.io.graph.yielder.nt_triples_yielder import NtTriplesYielder
from dbshx.io.graph.yielder.base_triples_yielder import BaseTriplesYielder


class MultiNtTriplesYielder(BaseTriplesYielder):

    def __init__(self, list_of_files, namespaces_to_ignore=None, allow_untyped_numbers=False):
        super(MultiNtTriplesYielder, self).__init__()
        self._list_of_files = list_of_files
        self._triples_yielded_from_used_yielders = 0
        self._error_triples_from_used_yielders = 0
        self._namespaces_to_ignore = namespaces_to_ignore
        self._allow_untyped_numbers = allow_untyped_numbers

        self._last_yielder = None



    def yield_triples(self):
        self._reset_count()
        for a_source_file in self._list_of_files:
            # print "New file! --> ", a_source_file
            for a_triple in self._yield_triples_of_file(a_source_file):
                yield a_triple
        # print "Final number of triples: ", self.yielded_triples

    def _yield_triples_of_file(self, a_source_file):
        if self._last_yielder is not None:
            self._triples_yielded_from_used_yielders += self._last_yielder.yielded_triples
            self._error_triples_from_used_yielders += self._last_yielder.error_triples
        self._last_yielder = NtTriplesYielder(source_file=a_source_file,
                                              allow_untyped_numbers=self._allow_untyped_numbers,
                                              namespaces_to_ignore=self._namespaces_to_ignore)
        for a_triple in self._last_yielder.yield_triples():
            yield a_triple

    @property
    def yielded_triples(self):
        triples_current_yielder = 0 if self._last_yielder is None else self._last_yielder.triples_yielded()
        return self._triples_yielded_from_used_yielders + triples_current_yielder

    @property
    def error_triples(self):
        errors_current_yielder = 0 if self._last_yielder is None else self._last_yielder.error_triples()
        return self._error_triples_from_used_yielders  + errors_current_yielder

    def _reset_count(self):
        self._error_triples_from_used_yielders = 0
        self._triples_yielded_from_used_yielders = 0

