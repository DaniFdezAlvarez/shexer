from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker

class MixedInstanceTracker(AbstractInstanceTracker):

    def __init__(self, list_of_instance_trackers):
        self._reference_instance_tracker = list_of_instance_trackers[0]
        self._secondary_instance_trackers = [] if len(list_of_instance_trackers) <= 1 else list_of_instance_trackers[1:]
        self._disambiguator_counter = 0


    def track_instances(self):
        reference_instances_dict = self._reference_instance_tracker.track_instances()
        for a_tracker in self._secondary_instance_trackers:
            self._integrate_dicts(reference_dict=reference_instances_dict,
                                  new_dict=a_tracker.track_instances(),
                                  new_tracker=a_tracker)
        return reference_instances_dict


    def _integrate_dicts(self, reference_dict, new_dict, new_tracker):
        if not self._is_there_key_ambiguity(reference_iterable=reference_dict,
                                            new_iterable=new_dict):
            self._integrate_dicts_with_no_key_ambiguity(reference_dict=reference_dict,
                                                        new_dict=new_dict)
        else:
            self._integrate_dicts_with_key_ambiguity(reference_dict=reference_dict,
                                                     new_dict=new_dict,
                                                     new_tracker=new_tracker)


    def _is_there_key_ambiguity(self, reference_iterable, new_iterable):
        """
        If possible, provide in reference iterable a structure with O(1) for the 'in' operator

        :param reference_iterable:
        :param new_iterable:
        :return:
        """
        for a_new_key in new_iterable:
            if a_new_key in reference_iterable:
                return True
        return False

    def _integrate_dicts_with_no_key_ambiguity(self, reference_dict, new_dict):
        for a_new_key, a_new_value in new_dict.items():
            reference_dict[a_new_key] = a_new_value

    def _integrate_dicts_with_key_ambiguity(self, reference_dict, new_dict, new_tracker):
        prefix = self._get_disambiguator_prefix_label(reference_dict=reference_dict,
                                                      new_dict=new_dict,
                                                      new_tracker=new_tracker)
        for a_new_key, a_new_value in new_dict.items():
            reference_dict[prefix + a_new_key] = a_new_value

    def _get_disambiguator_prefix_label(self, reference_dict, new_dict, new_tracker):
        base_disam = new_tracker.disambiguator_prefix
        current_disam = base_disam
        new_keys = [current_disam + a_new_key for a_new_key in new_dict]
        while self._is_there_key_ambiguity(reference_iterable=reference_dict,
                                           new_iterable=new_keys):
            self._disambiguator_counter += 1
            current_disam = base_disam + str(self._disambiguator_counter)
            new_keys = [current_disam + a_new_key for a_new_key in new_dict]
        return base_disam








