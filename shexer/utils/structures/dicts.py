
_MIN_IRI_POS = 0
_EXAMPLE_ENTITY_POS = 1
_PROP_FEATURES_POS = 2


_POS_DIRECT = 0
_POS_INVERSE = 1


class ShapeExampleFeaturesDict(object):

    def __init__(self, track_inverse_features):
        self._base_dict = {}
        self._track_inverse_features = track_inverse_features
        self.has_constraint_example = self._has_constraint_example_inverse \
            if track_inverse_features \
            else self._has_constraint_example_no_inverse  # TODO CONTINUE HERE: init several methods w.r.t. track_inverse_features

    def set_shape_min_iri(self, shape_id, min_iri):
        if shape_id not in self._base_dict:
            self._init_shape(shape_id)
        self._base_dict[shape_id][_MIN_IRI_POS] = min_iri

    def shape_min_iri(self, shape_id):
        return self._base_dict[shape_id][_MIN_IRI_POS]

    def set_shape_example(self, shape_id, example_iri):
        self._base_dict[shape_id][_EXAMPLE_ENTITY_POS] = example_iri

    def shape_example(self, shape_id):
        return self._base_dict[shape_id][_EXAMPLE_ENTITY_POS]

    def _init_shape(self, shape_id):
        self._base_dict[shape_id] = [None, None, {} if not self._track_inverse_features else [{}, {}]]


    def has_constraint_example(self, shape_id, prop_id):
        raise NotImplementedError()

    def set_constraint_example(self, shape_id, prop):
        raise NotImplementedError()

    def set_constraint_example_no_inverse(self, shape_id, prop_id, example):
        self._base_dict[shape_id][_PROP_FEATURES_POS][prop_id] = example

    def set_constraint_example_inverse(self, shape_id, prop_id, example, inverse):
        self._base_dict[shape_id][_PROP_FEATURES_POS][_POS_INVERSE if inverse else _POS_DIRECT][prop_id] = example

    def _has_constraint_example_no_inverse(self, shape_id, prop_id):
        return prop_id in self._base_dict[shape_id][_PROP_FEATURES_POS]

    def _has_constraint_example_inverse(self, shape_id, prop_id, inverse):
        return  prop_id in self._base_dict[shape_id][_PROP_FEATURES_POS][_POS_INVERSE if inverse else _POS_DIRECT]