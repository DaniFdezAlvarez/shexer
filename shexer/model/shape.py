STARTING_CHAR_FOR_SHAPE_NAME = "%"


class Shape(object):

    def __init__(self, name, class_uri, statements, n_instances):
        self._name = name
        self._class_uri = class_uri
        self._statements = statements if statements is not None else []
        self._n_instances = n_instances
        # self._inverse_statements = inverse_statements if inverse_statements is not None else []
        self._sorting_callback = lambda x: x.probability
        self._n_direct_statements = self._count_direct_statements(statements)
        self._n_inverse_statements = len(statements) - self._n_direct_statements

    @property
    def name(self):
        return self._name

    @property
    def class_uri(self):
        return self._class_uri

    @property
    def n_statements(self):
        return len(self._statements)

    @property
    def n_direct_statements(self):
        return self._n_direct_statements

    @property
    def n_inverse_statements(self):
        return self._n_inverse_statements

    @property
    def n_instances(self):
        return self._n_instances

    # @property
    # def iri_pattern(self):
    #     return self._iri_pattern
    #
    # @iri_pattern.setter
    # def iri_pattern(self, value):
    #     self._iri_pattern = value

    @property
    def statements(self):
        return self._statements

    @property
    def direct_statements(self):
        return [a_statement for a_statement in self._statements if not a_statement.is_inverse]

    @property
    def inverse_statements(self):
        return [a_statement for a_statement in self._statements if a_statement.is_inverse]

    @statements.setter
    def statements(self, value):
        self._statements = value

    @direct_statements.setter
    def direct_statements(self, statements):
        self._statements = [a_statement for a_statement in self._statements if a_statement.is_inverse]
        for a_statement in statements:
            self._statements.append(a_statement)

    @inverse_statements.setter
    def inverse_statements(self, inverse_statements):
        self._statements = [a_statement for a_statement in self._statements if not a_statement.is_inverse]
        for a_statement in inverse_statements:
            self._statements.append(a_statement)

    def yield_direct_statements(self):
        for a_statement in self._statements:
            if not a_statement.is_inverse:
                yield a_statement

    def yield_inverse_statements(self):
        for a_statement in self._statements:
            if a_statement.is_inverse:
                yield a_statement

    def sort_statements(self, callback, reverse=False):
        self._statements.sort(key=lambda x: callback(x), reverse=reverse)


    def yield_statements(self, just_direct=False):
        if just_direct:
            for a_statement in self.yield_direct_statements():
                yield a_statement
        else:
            for a_statement in self._statements:
                yield a_statement

    @staticmethod
    def _count_direct_statements(statements):
        counter = 0
        for a_statement in statements:
            if not a_statement.is_inverse:
                counter += 1
        return counter

