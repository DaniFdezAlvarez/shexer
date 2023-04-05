from shexer.core.shexing.strategy.minimal_iri_strategy.abstract_min_iri_strategy import AbstractMinIriStrategy

class AnnotateMinIriStrategy(AbstractMinIriStrategy):


    def __init__(self, min_iris_dict):
        self._min_iris_dict = min_iris_dict

    def annotate_shape_iri(self, shape):
        shape.iri_pattern = self._min_iris_dict[shape.class_uri]
