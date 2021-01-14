from shexer.utils.shapes import build_shapes_name_for_class_uri

def determine_original_target_nodes_if_needed(remove_empty_shapes, original_target_classes, original_shape_map, shapes_namespace):
    if not remove_empty_shapes:
        return None  # We dont need this structure if there are no shapes to remove.
    result = set()
    if original_target_classes is not None:
        for a_class in original_target_classes:
            result.add(build_shapes_name_for_class_uri(class_uri=a_class,
                                                       shapes_namespace=shapes_namespace))
    if original_shape_map is not None:
        for an_item in original_shape_map.yield_items():
            result.add(an_item.shape_label)
    return result