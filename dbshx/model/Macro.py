
from dbshx.model.const_elem_types import *

_VALID_MACROS = [IRI_ELEM_TYPE, LITERAL_ELEM_TYPE, DOT_ELEM_TYPE, BNODE_ELEM_TYPE]

class Macro(object):
    def __init__(self, macro_const):
        if macro_const not in _VALID_MACROS:
            print _VALID_MACROS
            print macro_const == DOT_ELEM_TYPE
            raise ValueError("Not recognized macro: " + macro_const)
        self._macro_representation = macro_const

    def __str__(self):
        return self._macro_representation

    @property
    def elem_type(self):
        return self._macro_representation

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return str(other) == str(self)

    def __neq__(self, other):
        pass

        # def __init__(self, content):
        #     self._content = content
        #
        # def __str__(self):
        #     return self._content
        #
        # @property
        # def elem_type(self):
        #     return IRI_ELEM_TYPE
        #
        # @property
        # def iri(self):
        #     return self._content
        #
        # def __eq__(self, other):
        #     if type(other) != type(self):
        #         return False
        #     return str(self) == str(other)