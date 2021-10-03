from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from shexer.utils.uri import remove_corners, unprefixize_uri_mandatory
from shexer.utils.triple_yielders import tune_subj, tune_prop, tune_token
import re

_OTHER_BLANKS = re.compile("[\r\n\t]")
_SEVERAL_BLANKS = re.compile("  +")
_QUOTES_FOR_LITERALS = re.compile('[^\\\]"')
_INIT_INLINE_COMMENT = re.compile(" #")
_RDF_TYPE_CONTRACTED = ["a", "rdf:type"]
_RDF_TYPE_URI = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"
_BOOLEANS = ["true", "false"]
_INI_BASE_URIS = ["/", "#"]

"""
TTL parser that yield triples (model objects) without loading the whole graph content in 
main memory.

WARNING: This parser works with some frequent structural assumptions of turtle files that
are not part of the standard. You may get unexpected errors or unexpected results dealing
with files containing lines which represent more than one triple. Also, we assume a totally
wel--formated input. Bad-formatted may remain undetected and produce wrong triples.

Please, in case you do not need to parse huge files that do not fit in the main memory
of your computer, use RdflifTriplesYielder instead
"""


class BigTtlTriplesYielder(BaseTriplesYielder):

    def __init__(self, source_file=None, allow_untyped_numbers=True, raw_graph=None):

        super(BigTtlTriplesYielder, self).__init__()
        self._source_file = source_file
        self._raw_graph = raw_graph
        self._triples_count = 0
        self._error_triples = 0
        self._allow_untyped_numbers = allow_untyped_numbers
        self._line_reader = self._decide_line_reader(source_file=source_file,
                                                     raw_graph=raw_graph)
        # Support
        self._prefixes = {}
        self._base = None

        # To be used while parsing
        self._tmp_s = None
        self._tmp_p = None
        self._tmp_o = None
        self._last_triple_jump = None

        self._triple_ready = False

    def yield_triples(self):
        self._reset_count()
        for a_line in self._line_reader.read_lines():
            self._process_line(a_line)
            if self._triple_ready:
                self._triples_count += 1
                # print("Wue")
                yield (
                    tune_subj(self._tmp_s),
                    tune_prop(self._tmp_p),
                    tune_token(self._tmp_o,
                               base_namespace=self._base,
                               allow_untyped_numbers=self._allow_untyped_numbers)
                )
                # print("Wuo!")
                # print( tune_subj(self._tmp_s),
                #     tune_prop(self._tmp_p),
                #     tune_token(self._tmp_o,
                #                base_namespace=self._base))
                self._triple_ready = False


    def _clean_line(self, str_line):
        result = _OTHER_BLANKS.sub(" ", str_line)
        result = _SEVERAL_BLANKS.sub(" ", result)
        result = result.strip()
        return result if " #" not in result else self._remove_comments_if_needed(result)

    def _remove_comments_if_needed(self, str_line):
        """Remove comments in the middle of the line.
        Lines starting with # wont be erased
        """
        if '"' not in str_line:  # Comment mark and no literals, trivial case
            return str_line[:str_line.find(" #")]
        # We need to find the begining and end of the literal to avoid erasing
        # comments whithin literals (actual content)
        quotes_indexes = []
        count_down_quotes = 2
        for a_match in _QUOTES_FOR_LITERALS.finditer(str_line):
            quotes_indexes.append(a_match.start(0))
            count_down_quotes -= 1
            if count_down_quotes == 0:
                break
        for a_match in _INIT_INLINE_COMMENT.finditer(str_line):
            if a_match.start(0) < quotes_indexes[0] or a_match.start(0) > quotes_indexes[1]:
                return str_line[:a_match.start(0)]
        return str_line  # If this point is reached, it means that the potential comments
                         # are actual content of a string literal




    def _process_line(self, str_line):
        str_line = self._clean_line(str_line)
        if str_line == "":
            self._process_empty_line(str_line)
        elif '"' in str_line:
            self._process_line_with_literal(str_line)
        elif str_line.startswith("@prefix"):
            self._process_prefix_line(str_line)
        elif str_line.startswith("@base"):
            self._process_base_line(str_line)
        elif str_line.startswith("#"):
            self._process_comment_line(str_line)
        elif str_line[-1] in [",", ".", ";"]:
            if ", " in str_line[:-1]:
                # If there is a comma in a URI, it can't be followed by a blank
                self._process_multi_triple_line_commas(str_line)
            else:
                self._process_single_triple_line(str_line)
        elif " " not in str_line:
            if len(str_line) > 1:  # We are ensuring that this is not a single char, such as "," or "."
                self._process_isolated_subject(str_line)
        else:
            self._process_unknown_line(str_line)

    def _process_line_with_literal(self, line):
        first_quotes_index = line.find('"')
        s_o_line = line[:first_quotes_index].strip()
        s_o_pieces = s_o_line.split(" ")
        if len(s_o_pieces) == 2:
            self._tmp_s = self._parse_elem(s_o_pieces[0])
            self._tmp_p = self._parse_elem(s_o_pieces[1])
        elif len(s_o_pieces) == 1 and s_o_pieces[0] != "":
            self._tmp_p = self._parse_elem(s_o_pieces[0])
        # The last char MUST be in [,.;] since this lines comes stripped.
        # SO everything between first_quotes_index and line[-1], stripped
        # should be out target literal (typed or not)
        self._tmp_o = line[first_quotes_index:-1].rstrip()
        self._decide_current_triple()

    def _process_prefix_line(self, line):
        pieces = line.split(" ")
        prefix = pieces[1] if not pieces[1].endswith(":") else pieces[1][: - 1]
        base_url = remove_corners(pieces[2])
        self._prefixes[prefix] = base_url

    def _process_base_line(self, line):
        pieces = line.split(" ")
        # base_url = pieces[1] if not pieces[1].endswith(":") else pieces[1][: - 1]
        # base_url = remove_corners(pieces[2])
        self._base = remove_corners(pieces[1])

    def _process_comment_line(self, line):
        pass  # At this point, just ignore it.

    def _process_empty_line(self, line):
        pass  # At this point, just ignore it.

    def _process_unknown_line(self, line):
        self._error_triples += 1


    def _process_multi_triple_line_commas(self, line):
        pieces = line.split(" ")
        index_first_comma = 0
        for i in range(0, len(pieces)):
            if pieces[i] == ",":
                index_first_comma = i
                break
        if index_first_comma == 3:
            self._tmp_s = self._parse_elem(pieces[0])
            self._tmp_p = self._parse_elem(pieces[1])
            self._tmp_o = self._parse_elem(pieces[2])
        elif index_first_comma == 2:
            self._tmp_p = self._parse_elem(pieces[0])
            self._tmp_o = self._parse_elem(pieces[1])
        elif index_first_comma == 1:
            self._tmp_o = self._parse_elem(pieces[0])
        # else impossible?
        self._decide_current_triple()

        for i in range(index_first_comma + 2, len(pieces), 2):
            self._tmp_o = self._parse_elem(pieces[i - 1])
            self._decide_current_triple()

    def _process_single_triple_line(self, line):
        pieces = line.split(" ")
        if len(pieces) == 4:
            self._tmp_s = self._parse_elem(pieces[0])
            self._tmp_p = self._parse_elem(pieces[1])
            self._tmp_o = self._parse_elem(pieces[2])

        elif len(pieces) == 3:
            self._tmp_p = self._parse_elem(pieces[0])
            self._tmp_o = self._parse_elem(pieces[1])
        elif len(pieces) == 2:
            self._tmp_o = self._parse_elem(pieces[0])
        self._decide_current_triple()

    def _process_isolated_subject(self, line):
        # No splitt. Line is expected to contain a line with no blanks (isolated subject)
        self._tmp_s = self._parse_elem(line)
        # No need to decide triple now, incomplete element

    def _decide_current_triple(self):
        # if self._is_bnode(self._tmp_s):
        #     self._ignored_triples += 1
        # elif self._is_bnode(self._tmp_o):
        #     self._ignored_triples += 1
        # elif self._is_num_literal(self._tmp_o):
        #     self._ignored_triples += 1
        # elif self._is_boolean(self._tmp_o):
        #     self._ignored_triples += 1
        # else:
        self._triple_ready = True

    def _is_boolean(self, raw_element):
        return True if raw_element in _BOOLEANS else False

    def _is_bnode(self, a_elem):
        if a_elem[0] == "_":
            return True
        return False

    def _is_num_literal(self, elem):
        try:
            float(elem)
            return True
        except ValueError:
            return False

    def _parse_elem(self, raw_elem):
        if raw_elem[0] == "<":
            return self._parse_cornered_element(raw_elem)
        elif raw_elem in _RDF_TYPE_CONTRACTED:
            return _RDF_TYPE_URI
        elif ":" in raw_elem:
            return unprefixize_uri_mandatory(target_uri=raw_elem,
                                             prefix_namespaces_dict=self._prefixes)
        elif raw_elem in _BOOLEANS or self._is_num_literal(raw_elem):
            return raw_elem
            # else?? shouldnt happen, let it break with a nullpoitner

    def _parse_cornered_element(self, cornered_element):
        if self._base is None:
            return cornered_element  # There is no base
        elif cornered_element[1] in _INI_BASE_URIS:
            return "<" + self._base + cornered_element[2:-1] + ">"
        elif not cornered_element[1:].startswith("http"):
            return "<" + self._base + cornered_element[1:-1] + ">"
        else:
            return cornered_element  # Nothing to do with base

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_triples

    @property
    def ignored_triples(self):
        return self._ignored_triples

    def _reset_count(self):
        self._error_triples = 0
        self._triples_count = 0
        self._ignored_triples = 0


