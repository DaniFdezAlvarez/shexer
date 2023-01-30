from shexer.io.shex.formater.statement_serializers.frequency_strategy.base_frequency_strategy import BaseFrequencyStrategy
import math


class RatioFreqSerializer(BaseFrequencyStrategy):

    def __init__(self, decimals=-1):
        self._decimals=-1
        if decimals < 0:
            self.serialize_frequency = self._serialize_freq_unbounded
        else:
            self.serialize_frequency = self._serialize_freq_decimals


    def serialize_frequency(self, statement):
        raise NotImplementedError("This function will be initialized with a callback during the __init__")

    def _serialize_freq_unbounded(self, statement):
        return str(statement.probability * 100) + "%"

    def _serialize_freq_decimals(self, statement):
        return str(round(statement.probability, self._decimals)) + "%"
