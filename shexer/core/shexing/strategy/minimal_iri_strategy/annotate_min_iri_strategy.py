from shexer.core.shexing.strategy.minimal_iri_strategy.abstract_min_iri_strategy import AbstractMinIriStrategy
import re

_SEP_CHARS = re.compile("[:/#]")


class AnnotateMinIriStrategy(AbstractMinIriStrategy):

    def __init__(self, min_iris_dict):
        self._min_iris_dict = min_iris_dict

    def annotate_shape_iri(self, shape):
        self._min_iris_dict.set_shape_min_iri(shape_id=shape.class_uri,
                                              min_iri=self._determine_suitable_iri_pattern
                                                  (
                                                  self._min_iris_dict.shape_min_iri
                                                      (
                                                      shape.class_uri
                                                      )
                                                  )
                                              )
        # shape.iri_pattern = self._determine_suitable_iri_pattern(self._min_iris_dict.shape_min_iri(shape.class_uri))
        # shape.iri_pattern = self._determine_suitable_iri_pattern(self._min_iris_dict[shape.class_uri])

    def _determine_suitable_iri_pattern(self, longest_common_prefix):
        backwards_str = longest_common_prefix[::-1]
        last_sep_char = _SEP_CHARS.search(backwards_str)
        if last_sep_char is None:
            return None
        candidate_min_iri = backwards_str[last_sep_char.start():][::-1]
        if len(candidate_min_iri) < 3:  # Just too short. Kind of an arbitrary number
            return None
        if candidate_min_iri.startswith("http") and len(candidate_min_iri) < 8:  # http:// or https:// + an extra char
            return None
        return candidate_min_iri  # Let's say it is a worthy one
