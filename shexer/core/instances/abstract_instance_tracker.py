from shexer.model.property import Property
from shexer.utils.uri import remove_corners
from shexer.utils.factories.h_tree import get_basic_h_tree

_TRACKERS_DISAM_COUNT = 0

_RDF_TYPE = Property(content="http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
_RDFS_SUBCLASS_OF = Property(content="http://www.w3.org/2000/01/rdf-schema#subClassOf")

class AbstractInstanceTracker(object):

    def track_instances(self, verbose=False):
        raise NotImplementedError()


    @property
    def disambiguator_prefix(self):
        """
        It returns a str that may help for disambiguation purposes if the instance_tracker is used to produce dicts
        that may be integrated with other instance dicts and there should be any key colission.
        :return:
        """
        global _TRACKERS_DISAM_COUNT
        _TRACKERS_DISAM_COUNT += 1
        return self._specific_disambiguator_prefix() + str(_TRACKERS_DISAM_COUNT )

    def _specific_disambiguator_prefix(self):
        raise NotImplementedError()

    @staticmethod
    def _build_instances_dict():
        return {}  # Empty in every case. Instances, on the fly, will be the keys

    @staticmethod
    def _decide_instantiation_property(instantiation_property):
        if instantiation_property == None:
            return _RDF_TYPE
        if type(instantiation_property) == type(_RDF_TYPE):
            return instantiation_property
        if type(instantiation_property) == str:
            return Property(remove_corners(a_uri=instantiation_property,
                                           raise_error_if_no_corners=False))
        raise ValueError("Unrecognized param type to define instantiation property")

    def _reset_count(self):
        self._relevant_triples = 0
        self._not_relevant_triples = 0
        self._htree = get_basic_h_tree()

