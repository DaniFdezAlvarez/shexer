from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker
from shexer.utils.log import log_msg

class MixedInstanceTracker(AbstractInstanceTracker):

    def __init__(self, list_of_instance_trackers):
        self._reference_instance_tracker = list_of_instance_trackers[0]
        self._secondary_instance_trackers = [] if len(list_of_instance_trackers) <= 1 else list_of_instance_trackers[1:]
        self._disambiguator_counter = 0

    def track_instances(self, verbose=True):
        log_msg(verbose=verbose,
                msg="Starting instance tracking process with a MixedInstance tracker. "
                    "Several Instance Trackers may be launched...")
        reference_instances_dict = self._reference_instance_tracker.track_instances(verbose=verbose)
        for a_tracker in self._secondary_instance_trackers:
            self._integrate_dicts(reference_dict=reference_instances_dict,
                                  new_dict=a_tracker.track_instances(verbose=verbose),
                                  new_tracker=a_tracker)
        log_msg(verbose=verbose,
                msg="Every instance tracker has finished and their results have been integrated."
                    " {} instances have been located".format(len(reference_instances_dict)))
        return reference_instances_dict

    def _specific_disambiguator_prefix(self):
        return "mixed_"

    def _integrate_dicts(self, reference_dict, new_dict, new_tracker):
        original_classes = self._find_all_classes_in_dict(reference_dict)
        for an_instance, classes in new_dict.items():
            if an_instance not in reference_dict:
                reference_dict[an_instance] = []
            for a_class in classes:
                if a_class in original_classes:  # There is key_ambigüity, two trackers have
                                                 # identhical names for different elements
                    reference_dict[an_instance].append(self._get_label_for_ambiguous_class(a_class=a_class,
                                                                                           tracker=new_tracker))
                else:
                    reference_dict[an_instance].append(a_class)


    def _find_all_classes_in_dict(self, instances_dict):
        result = set()
        for classes in instances_dict.values():
            for a_class in classes:
                result.add(a_class)
        return result



    def _get_label_for_ambiguous_class(self, a_class, tracker):
        return tracker.disambiguator_prefix + a_class









