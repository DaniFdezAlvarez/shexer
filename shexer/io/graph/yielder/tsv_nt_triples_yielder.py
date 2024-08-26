from shexer.utils.log import log_msg
from shexer.utils.triple_yielders import tune_token, tune_prop
from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder


class TsvNtTriplesYielder(BaseTriplesYielder):

    def __init__(self, source_file, allow_untyped_numbers=False, raw_graph=None,
                 compression_mode=None, zip_base_archive=None):
        super(TsvNtTriplesYielder, self).__init__()
        self._source_file = source_file
        self._triples_count = 0
        self._error_triples = 0
        self._allow_untyped_numbers = allow_untyped_numbers
        self._line_reader = self._decide_line_reader(source_file=source_file,
                                                     raw_graph=raw_graph,
                                                     compression_mode=compression_mode,
                                                     zip_base_archive=zip_base_archive)
        # self.yield_triples = self._yield_triples_not_excluding_namespaces if namespaces_to_ignore is None\
        #     else self._yield_triples_excluding_namespaces


    def yield_triples(self):
        self._reset_count()
        for a_line in self._line_reader.read_lines():
            tokens = self._look_for_tokens(a_line.strip())
            if len(tokens) != 3:
                self._error_triples += 1
                log_msg(msg="This line caused error: " + a_line,
                             source=self._source_file)
            else:
                try:
                    yield (
                    tune_token(tokens[0]), tune_prop(tokens[1]), tune_token(tokens[2], allow_untyped_numbers=True))
                    self._triples_count += 1
                except ValueError as ve:
                    log_msg(msg=ve.message + "This line caused error: " + a_line,
                                 source=self._source_file)
                # if self._triples_count % 10000 == 0:
                #     print("Reading..." + self._triples_count)

    def _look_for_tokens(self, str_line):
        return str_line.split("\t")

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_triples

    def _reset_count(self):
        self._error_triples = 0
        self._triples_count = 0

    # def yield_triples(self):
    #     self._reset_parsing()
    #     for a_line in self._line_reader.read_lines():
    #         tokens = self._look_for_tokens(a_line.strip())
    #         if len(tokens) != 3:
    #             self._error_triples += 1
    #             log_msg(msg="This line caused error: " + a_line,
    #                          source=self._source_file)
    #         else:
    #             try:
    #                 yield (tune_token(tokens[0]),
    #                        tune_prop(tokens[1]),
    #                        tune_token(tokens[2], allow_untyped_numbers=self._allow_untyped_numbers))
    #                 self._triples_count += 1
    #             except ValueError as ve:
    #                 log_msg(msg=ve.message + "This line caused error: " + a_line,
    #                              source=self._source_file)
    #             if self._triples_count % 10000 == 0:
    #                 print("Reading..." + self._triples_count)

    # def _yield_triples_excluding_namespaces(self):
    #     self._reset_parsing()
    #     for a_line in self._line_reader.read_lines():
    #         tokens = self._look_for_tokens(a_line.strip())
    #         if len(tokens) != 3:
    #             self._error_triples += 1
    #             log_msg(msg="This line caused error: " + a_line,
    #                          source=self._source_file)
    #         else:
    #             try:
    #                 candidate_triple = (tune_token(tokens[0]),
    #                                     tune_prop(tokens[1]),
    #                                     tune_token(tokens[2], allow_untyped_numbers=True))
    #                 if not check_if_property_belongs_to_namespace_list(str(candidate_triple[1]),
    #                                                                    namespaces=self._namespaces_to_ignore):
    #                     yield candidate_triple
    #
    #                 self._triples_count += 1
    #             except ValueError as ve:
    #                 log_msg(msg=ve.message + "This line caused error: " + a_line,
    #                              source=self._source_file)
    #             if self._triples_count % 10000 == 0:
    #                 print("Reading..." + self._triples_count)
