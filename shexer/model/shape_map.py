

class ShapeMap(object):

    def __init__(self, shape_map_items=None):
        self._items = shape_map_items if shape_map_items is not None else []


    def add_item(self, shape_map_item):
        self._items.append(shape_map_item)


    def yield_items(self):
        for an_item in self._items:
            yield an_item

    def get_sgraph(self):
        if len(self._items) == 0:
            return None
        return self._items[0].node_selector.sgraph  # Assuming they all have the same sgraph


class ShapeMapItem(object):

    def __init__(self, node_selector, shape_label):
        self._node_selector = node_selector
        self._shape_label = shape_label

    @property
    def node_selector(self):
        return self._node_selector

    @property
    def shape_label(self):
        return self._shape_label