"""
CAUTION! This yielder is able to parse a huge file without loading the whole graph in memory,
but it is expecting a perfectly well-formed ttl. Syntax errors may cause unpredicted failures.

Also, it is ignoring b-nodes, which does not neccesarily make sense for all the sources.
If you want to include bnodes in your classrank computation, you should use/implement
a different yielder.

"""

from dbshx.utils.log import log_to_error
from dbshx.utils.uri import remove_corners, parse_literal
from dbshx.model.IRI import IRI
from dbshx.model.literal import Literal
from dbshx.model.bnode import BNode
from dbshx.model.property import Property

# import re
#
# from src.pyonto_utils.uri import remove_corners, parse_float
# from src.pyonto_utils.log import log_to_error
#
# _SEVERAL_BLANKS = re.compile("[ \r\n\t][ \r\n\t]+")
# _RDF_TYPE = "rdf:type"
# _BOOLEANS = ["true", "false"]


class TtlTriplesYielder(object):
    def __init__(self, source_file):
        self._source_file = source_file
        self._triples_count = 0
        self._error_triples = 0


    def yield_triples(self):
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                pieces = a_line.strip().split(" ")
                if len(pieces) != 4:
                    self._error_triples += 1
                    log_to_error(msg="This line caused error: " + a_line,
                                 source=self._source_file)
                else:
                    yield (self._tune_token(pieces[0]), self._tune_prop(pieces[1]), self._tune_token(pieces[2]))
                    self._triples_count += 1
                    # if self._triples_count % 100000 == 0:
                    #     print "Reading...", self._triples_count


    def _tune_token(self, a_token):
        if a_token.startswith("<"):
            return IRI(remove_corners(a_token))
        elif a_token.startswith('"'):
            content, elem_type = parse_literal(a_token)
            return Literal(content=content,
                           elem_type=elem_type)
        else:  # a BNode
            return BNode(identifier=a_token)


    def _tune_prop(self, a_token):
        return Property(remove_corners(a_token))


    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_triples

    def _reset_count(self):
        self._error_triples = 0
        self._triples_count = 0

