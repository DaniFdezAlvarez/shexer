
_IRI_ELEM_TYPE = "IRI"

class IRI(object):

    def __init__(self, content):
        self._content = content

    def __str__(self):
        return self._content

    def elem_type(self):
        return _IRI_ELEM_TYPE