from shexer.core.shexing.strategy.minimal_iri_strategy.abstract_min_iri_strategy import AbstractMinIriStrategy


class IgnoreMinIriStrategy(AbstractMinIriStrategy):

    def __init__(self):
        pass

    def annotate_shape_iri(self, shape):
        """
        Just skip this, no need to do anything

        :param shape:
        :param class_key:
        :return:
        """
        pass
