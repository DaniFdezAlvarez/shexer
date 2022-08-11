from shexer.io.graph.yielder.multifile_base_triples_yielder import MultifileBaseTripleYielder
from shexer.io.graph.yielder.rdflib_triple_yielder import RdflibParserTripleYielder
from shexer.consts import TURTLE


class MultiRdfLibTripleYielder(MultifileBaseTripleYielder):

    def __init__(self, list_of_files, input_format=TURTLE, allow_untyped_numbers=False,
                 namespaces_dict=None, compression_mode=None, zip_archive_file=None):
        super(MultiRdfLibTripleYielder, self).__init__(list_of_files=list_of_files,
                                                       allow_untyped_numbers=allow_untyped_numbers)

        self._input_format = input_format
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._compression_mode = compression_mode
        self._zip_archive_file = zip_archive_file

    def _yield_triples_of_last_yielder(self, parse_namespaces=True):
        for a_triple in self._last_yielder.yield_triples(parse_namespaces):
            yield a_triple

    def _constructor_file_yielder(self, a_source_file):
        return RdflibParserTripleYielder(source=a_source_file,
                                         allow_untyped_numbers=self._allow_untyped_numbers,
                                         input_format=self._input_format,
                                         compression_mode=self._compression_mode,
                                         zip_archive_file=self._zip_archive_file)

    @property
    def namespaces(self):
        return self._namespaces_dict  # TODO This is not entirely correct. But this method will be rarely used
        # and can have a huge performance cost in case the graphs hadnt been parsed yet
