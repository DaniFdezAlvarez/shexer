
class BaseFrequencyStrategy(object):


    def serialize_frequency(self, statement):
        raise NotImplementedError("This should be implemented in child classes")