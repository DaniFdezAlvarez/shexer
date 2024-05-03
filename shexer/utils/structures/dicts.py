
_MIN_IRI_POS = 0
_EXAMPLE_ENTITY_POS = 1
_PROP_FEATURES_POS = 2

class ShapeExampleFeaturesDict(object):

    def __init__(self):
        self._base_dict = {}

    def set_shape_min_iri(self, shape_id, min_iri):
        if shape_id not in self._base_dict:
            self._init_shape(shape_id)
        self._base_dict[shape_id][_MIN_IRI_POS] = min_iri

    def shape_min_iri(self, shape_id):
        return self._base_dict[shape_id][_MIN_IRI_POS]

    def set_shape_example(self, shape_id, example_iri):
        pass

    def shape_example(self, shape_iri):
        pass

    def _init_shape(self, shape_id):
        self._base_dict[shape_id] = [None, None, {}]