from dbshx.io.graph.yielder.multi_nt_triples_yielder import MultiNtTriplesYielder
from dbshx.io.graph.yielder.nt_triples_yielder import NtTriplesYielder
from dbshx.consts import NT


def get_triple_yielder(source_file=None, list_of_source_files=None, input_format=NT):
    if input_format == NT:
        if source_file is not None:
            return NtTriplesYielder(source_file=source_file)
        else:
            return MultiNtTriplesYielder(list_of_files=list_of_source_files)
    raise ValueError("Not supported format: " + NT)