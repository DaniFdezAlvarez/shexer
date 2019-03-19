from dbshx.io.graph.yielder.multi_nt_triples_yielder import MultiNtTriplesYielder
from dbshx.io.graph.yielder.nt_triples_yielder import NtTriplesYielder
from dbshx.io.graph.yielder.tsv_nt_triples_yielder import TsvNtTriplesYielder
from dbshx.io.graph.yielder.multi_tsv_nt_triples_yielder import MultiTsvNtTriplesYielder

from dbshx.consts import NT, TSV_SPO


def get_triple_yielder(source_file=None, list_of_source_files=None, input_format=NT, namespaces_to_ignore=None,
                       allow_untyped_numbers=False, raw_graph=None):
    if input_format == NT:
        if source_file is not None or raw_graph is not None:
            return NtTriplesYielder(source_file=source_file,
                                    namespaces_to_ignore=namespaces_to_ignore,
                                    allow_untyped_numbers=allow_untyped_numbers,
                                    raw_graph=raw_graph)
        else:
            return MultiNtTriplesYielder(list_of_files=list_of_source_files,
                                         namespaces_to_ignore=namespaces_to_ignore,
                                         allow_untyped_numbers=allow_untyped_numbers)
    if input_format == TSV_SPO:
        if source_file is not None or raw_graph is not None:
            return TsvNtTriplesYielder(source_file=source_file,
                                       namespaces_to_ignore=namespaces_to_ignore,
                                       allow_untyped_numbers=allow_untyped_numbers,
                                       raw_graph=raw_graph)
        else:
            return MultiTsvNtTriplesYielder(list_of_files=list_of_source_files,
                                            namespaces_to_ignore=namespaces_to_ignore,
                                            allow_untyped_numbers=allow_untyped_numbers)

    raise ValueError("Not supported format: " + input_format)
