STARTING_CHAR_FOR_SHAPE_NAME = "@"


class Shape(object):

    def __init__(self, name, class_uri, statements, inverse_statements=None):
        self._name = name
        self._class_uri = class_uri
        self._statements = statements
        self._inverse_statements = inverse_statements if inverse_statements is not None else []
        self._sorting_callback = None

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
        d_pos = i_pos = 0
        next_direct = self._statements[d_pos] if d_pos < len(self._statements) else None
        next_inverse = self._inverse_statements[d_pos] if i_pos < len(self._inverse_statements) else None
        while next_direct is not None or next_inverse is not None:
            if next_inverse is None:
                yield next_direct
                d_pos += 1
            elif next_direct is None:
                yield next_inverse
                i_pos += 1
            else:
                d_score = self._sorting_callback(next_direct)
                i_score = self._sorting_callback(next_inverse)
                if (d_score >= i_score and reverse) or (d_score <= i_score and not reverse):
                    yield next_direct
                    d_pos += 1
                else:
                    yield next_inverse
                    i_pos += 1

    def yield_direct_statements(self):
        for a_statement in self._statements:
            yield a_statement

    def yield_inverse_statements(self):
        for a_statement in self._inverse_statements:
            yield a_statement

    def sort_statements(self, callback, reverse=False):
        self._statements.sort(key=lambda x :callback(x), reverse=reverse)
        self._inverse_statements.sort(key=lambda x: callback(x), reverse=reverse)
