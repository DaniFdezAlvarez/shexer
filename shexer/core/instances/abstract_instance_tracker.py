
class AbstractInstanceTracker(object):

    def track_instances(self):
        raise NotImplementedError()


    @property
    def disambiguator_prefix(self):
        """
        It return an str that may help for disambiguation purposes if the instance_tracker is used to produce dicts
        that may be integrated with other instance dicts and there should be any key colission.
        :return:
        """
        raise NotImplementedError()

    @property
    def disambiguator_prefix(self):
        return "mixed_"