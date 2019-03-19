STARTING_CHAR_FOR_SHAPE_NAME = "@"


class Shape(object):

    def __init__(self, name, class_uri, statements):
        self._name = name
        self._class_uri = class_uri
        self._statements = statements

    @property
    def name(self):
        return self._name

    @property
    def class_uri(self):
        return self._class_uri

    def yield_statements(self):
        for a_statement in self._statements:
            yield a_statement


    def sort_statements(self, callback, reverse=False):
        self._statements.sort(key=lambda x :callback(x), reverse=reverse)
