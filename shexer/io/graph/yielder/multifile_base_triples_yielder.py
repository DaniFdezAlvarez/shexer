from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder


class MultifileBaseTripleYielder(BaseTriplesYielder):

    def __init__(self, list_of_files,
                 namespaces_to_ignore=None,
                 allow_untyped_numbers=False,
                 compression_mode=None,
                 zip_base_archive=None):
        super(BaseTriplesYielder, self).__init__()
        self._list_of_files = list_of_files
        self._namespaces_to_ignore = namespaces_to_ignore
        self._allow_untyped_numbers = allow_untyped_numbers
        self._compression_mode = compression_mode
        self._zip_base_archive = zip_base_archive

        self._triples_yielded_from_used_yielders = 0
        self._error_triples_from_used_yielders = 0
        self._last_yielder = None


    def yield_triples(self, parse_namespaces=True):
        self._reset_count()
        for a_source_file in self._list_of_files:
            for a_triple in self._yield_triples_of_file(a_source_file, parse_namespaces):
                yield a_triple

    def _yield_triples_of_file(self, a_source_file, parse_namespaces=False):
        if self._last_yielder is not None:
            self._triples_yielded_from_used_yielders += self._last_yielder.yielded_triples
            self._error_triples_from_used_yielders += self._last_yielder.error_triples
        self._last_yielder = self._constructor_file_yielder(a_source_file=a_source_file)
        for a_triple in self._yield_triples_of_last_yielder(parse_namespaces):
            yield a_triple

    @property
    def yielded_triples(self):
        triples_current_yielder = 0 if self._last_yielder is None else self._last_yielder.yielded_triples
        return self._triples_yielded_from_used_yielders + triples_current_yielder

    @property
    def error_triples(self):
        errors_current_yielder = 0 if self._last_yielder is None else self._last_yielder.error_triples
        return self._error_triples_from_used_yielders  + errors_current_yielder

    def _reset_count(self):
        self._error_triples_from_used_yielders = 0
        self._triples_yielded_from_used_yielders = 0

    def _constructor_file_yielder(self, a_source_file):
        raise NotImplementedError("Implement in derived classes")
        
    def _yield_triples_of_last_yielder(self, parse_namespaces=True):
        """
        This is a default implementation for every yielrder (most of them) which ignores parse_namespaces
        :param parse_namespaces:
        :return:
        """
        for a_triple in self._last_yielder.yield_triples():
            yield a_triple



