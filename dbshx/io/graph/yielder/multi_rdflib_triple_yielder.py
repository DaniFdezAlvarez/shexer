from dbshx.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from dbshx.io.graph.yielder.rdflib_triple_yielder import RdflibTripleYielder
from dbshx.consts import TURTLE


class MultiRdfLibTripleYielder(BaseTriplesYielder):

    def __init__(self, list_of_files, input_format=TURTLE, namespaces_to_ignore=None, allow_untyped_numbers=False, namespaces_dict=None):
        super(MultiRdfLibTripleYielder, self).__init__()
        self._list_of_files = list_of_files
        self._triples_yielded_from_used_yielders = 0
        self._error_triples_from_used_yielders = 0
        self._namespaces_to_ignore = namespaces_to_ignore
        self._allow_untyped_numbers = allow_untyped_numbers
        self._input_format = input_format
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}

        self._last_yielder = None


    def yield_triples(self, parse_namespaces=True):
        self._reset_count()
        for a_source_file in self._list_of_files:
            for a_triple in self._yield_triples_of_file(a_source_file, parse_namespaces):
                yield a_triple

    def _yield_triples_of_file(self, a_source_file, parse_namespaces):
        if self._last_yielder is not None:
            self._triples_yielded_from_used_yielders += self._last_yielder.yielded_triples
            self._error_triples_from_used_yielders += self._last_yielder.error_triples
        self._last_yielder = RdflibTripleYielder(source_file=a_source_file,
                                                 allow_untyped_numbers=self._allow_untyped_numbers,
                                                 namespaces_to_ignore=self._namespaces_to_ignore,
                                                 input_format=self._input_format)
        for a_triple in self._last_yielder.yield_triples(parse_namespaces):
            yield a_triple

    @property
    def yielded_triples(self):
        triples_current_yielder = 0 if self._last_yielder is None else self._last_yielder.triples_yielded()
        return self._triples_yielded_from_used_yielders + triples_current_yielder

    @property
    def error_triples(self):
        errors_current_yielder = 0 if self._last_yielder is None else self._last_yielder.error_triples()
        return self._error_triples_from_used_yielders  + errors_current_yielder

    @property
    def namespaces(self):
        return self._namespaces_dict  # TODO This is not entirely correct. But this method will be rarely used
                                      # and can have a huge performance cost in case the graphs hadnt been parsed yet

    def _reset_count(self):
        self._error_triples_from_used_yielders = 0
        self._triples_yielded_from_used_yielders = 0
