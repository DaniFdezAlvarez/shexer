from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker


class ShapeMapInstanceTracker(AbstractInstanceTracker):

    def __init__(self, shape_map):
        self._shape_map = shape_map
        self._instances_dict = {}

    def track_instances(self):
        for an_item in self._shape_map.yield_items():
            self._solve_targets_of_an_item(an_item)
        return self._instances_dict

    def _solve_targets_of_an_item(self, an_item):
        self._instances_dict[an_item.shape_label] = an_item.node_selector.get_target_nodes()

    @property
    def disambiguator_prefix(self):
        return "custom_"