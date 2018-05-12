


class Statement(object):

    def __init__(self, st_property, st_type, cardinality, probability):
        self._st_property = st_property
        self._st_type = st_type
        self._cardinality = cardinality
        self._probability = probability


    @property
    def st_property(self):
        return self._st_property

    @property
    def st_type(self):
        return self._st_type

    @property
    def cardinality(self):
        return self._cardinality

    @property
    def probability(self):
        return self._probability



