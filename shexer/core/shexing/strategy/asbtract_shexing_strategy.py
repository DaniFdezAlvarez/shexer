

class AbstractShexingStrategy(object):

    def __init__(self, class_shexer):
        self._class_shexer = class_shexer
        pass

    def yield_base_shapes(self, acceptance_threshold):
        raise NotImplementedError()

    def _compute_frequency(self, number_of_instances, n_ocurrences_statement):
        return float(n_ocurrences_statement) / number_of_instances
