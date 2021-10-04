from shexer.model.const_elem_types import BNODE_ELEM_TYPE

class BNode(object):

    def __init__(self, identifier):
        self._identifier = identifier

    def __str__(self):
        return self._identifier

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return str(self) == str(other)

    @property
    def elem_type(self):
        return BNODE_ELEM_TYPE

    @property
    def iri(self):
        return self._identifier
