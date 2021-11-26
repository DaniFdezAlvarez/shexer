STARTING_CHAR_FOR_SHAPE_NAME = "@"


class Shape(object):

    def __init__(self, name, class_uri, statements, inverse_statements=None):
        self._name = name
        self._class_uri = class_uri
        self._statements = statements
        self._inverse_statements = inverse_statements if inverse_statements is not None else []
        self._sorting_callback = lambda x: x.probability

    @property
    def name(self):
        return self._name

    @property
    def class_uri(self):
        return self._class_uri

    @property
    def n_statements(self):
        return len(self._statements) + len(self._inverse_statements)

    @property
    def n_direct_statements(self):
        return len(self._statements)

    @property
    def n_inverse_statements(self):
        return len(self._inverse_statements)

    @property
    def statements(self):
        return self._statements

    @property
    def inverse_statements(self):
        return self._inverse_statements

    @statements.setter
    def statements(self, statements):
        self._statements = statements

    @inverse_statements.setter
    def inverse_statements(self, inverse_statements):
        self._inverse_statements = inverse_statements

    def yield_statements(self, just_direct=True, sorted=True, reverse=True):
        if just_direct:
            for a_statement in self.yield_direct_statements():
                yield a_statement
        else:
            for a_statement in self._yield_direct_and_inverse_statements(sorted=sorted, reverse=reverse):
                yield a_statement

    def _yield_direct_and_inverse_statements(self, sorted, reverse):
        if not sorted:
            for a_statement in self.yield_direct_statements():
                yield a_statement
            for a_statement in self.yield_inverse_statements():
                yield a_statement
        else:
            for a_statement in self._yield_sorted_direct_and_inverse_statements(reverse=reverse):
                yield a_statement

    def _yield_sorted_direct_and_inverse_statements(self, reverse):
        to_yield = self._statements + self._inverse_statements
        to_yield.sort(key=lambda x: self._sorting_callback(x), reverse=reverse)
        for a_statement in to_yield:
            yield a_statement

    def yield_direct_statements(self):
        for a_statement in self._statements:
            yield a_statement

    def yield_inverse_statements(self):
        for a_statement in self._inverse_statements:
            yield a_statement

    def sort_statements(self, callback, reverse=False):
        self._sorting_callback = callback
        self._statements.sort(key=lambda x :callback(x), reverse=reverse)
        self._inverse_statements.sort(key=lambda x: callback(x), reverse=reverse)
