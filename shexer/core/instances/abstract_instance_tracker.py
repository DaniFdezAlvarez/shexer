
_TRACKERS_DISAM_COUNT = 0

class AbstractInstanceTracker(object):

    def track_instances(self, verbose=False):
        raise NotImplementedError()


    @property
    def disambiguator_prefix(self):
        """
        It return an str that may help for disambiguation purposes if the instance_tracker is used to produce dicts
        that may be integrated with other instance dicts and there should be any key colission.
        :return:
        """
        global _TRACKERS_DISAM_COUNT
        _TRACKERS_DISAM_COUNT += 1
        return self._specific_disambiguator_prefix() + str(_TRACKERS_DISAM_COUNT )

    def _specific_disambiguator_prefix(self):
        raise NotImplementedError()