
class Literal(object):

    def __init__(self, content, elem_type):
        self._content = content
        self._elem_type = elem_type

    def __str__(self):
        return self._content

    @property
    def elem_type(self):
        return self._elem_type



