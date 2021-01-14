from shexer.core.instances.annotators.base_annotator import BaseAnnotator
from shexer.core.instances.annotators.annotator_tracking_instances import AnnotatorTrackingInstances

def get_proper_annotator(track_hierarchies, instance_tracker_ref):
    return BaseAnnotator(instance_tracker_ref) if not track_hierarchies \
        else AnnotatorTrackingInstances(instance_tracker_ref)