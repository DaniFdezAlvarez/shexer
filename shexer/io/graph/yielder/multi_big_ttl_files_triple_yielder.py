
from shexer.io.graph.yielder.big_ttl_triples_yielder import BigTtlTriplesYielder
from shexer.io.graph.yielder.multifile_base_triples_yielder import MultifileBaseTripleYielder


class MultiBigTtlTriplesYielder(MultifileBaseTripleYielder):

    def __init__(self, list_of_files, allow_untyped_numbers=False, compression_mode=None, zip_base_archive=None):
        super(MultiBigTtlTriplesYielder, self).__init__(list_of_files=list_of_files,
                                                        allow_untyped_numbers=allow_untyped_numbers,
                                                        zip_base_archive=zip_base_archive,
                                                        compression_mode=compression_mode)

    def _constructor_file_yielder(self, a_source_file, parse_namespaces=False):
        return BigTtlTriplesYielder(source_file=a_source_file,
                                    allow_untyped_numbers=self._allow_untyped_numbers,
                                    compression_mode=self._compression_mode,
                                    zip_base_archive=self._zip_base_archive)



