from shexer.io.shex.formater.statement_serializers.frequency_strategy.base_frequency_strategy import BaseFrequencyStrategy
from shexer.io.shex.formater.statement_serializers.frequency_strategy.abs_freq_serializer import AbsFreqSerializer
from shexer.io.shex.formater.statement_serializers.frequency_strategy.ratio_freq_serializer import RatioFreqSerializer

class MixedFrequencyStrategy(BaseFrequencyStrategy):

    def __init__(self, decimals=-1):
        self._abs_strategy = AbsFreqSerializer()
        self._ratio_strategy = RatioFreqSerializer(decimals=decimals)

    def serialize_frequency(self, statement):
        # The abs_strategy return a trailing dot that we want to skip. That why I use slicing here
        return self._ratio_strategy.serialize_frequency(statement) + \
               " (" + self._abs_strategy.serialize_frequency(statement)[:-1] + ")."


