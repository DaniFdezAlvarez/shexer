
from shexer.io.shex.formater.statement_serializers.frequency_strategy.base_frequency_strategy import BaseFrequencyStrategy

class AbsFreqSerializer(BaseFrequencyStrategy):

    def serialize_frequency(self, statement):
        return str(statement.n_occurences) + " instances"




