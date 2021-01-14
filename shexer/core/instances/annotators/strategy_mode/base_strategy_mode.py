class BaseStrategyMode(object):

    def __init__(self, annotator_ref):
        self._annotator_ref = annotator_ref
        self._instantiation_property = self._annotator_ref._instantiation_property
        self._instances_dict = self._annotator_ref._instances_dict
        self._instance_tracker = self._annotator_ref._instance_tracker

    def is_relevant_triple(self, a_triple):
        raise NotImplementedError()

    def annotate_triple(self, a_triple):
        raise NotImplementedError()

    def annotation_post_parsing(self):
        pass  # By default, do nothing.
