from shexer.utils.factories.triple_yielders_factory import get_triple_yielder
from shexer.core.class_profiler import ClassProfiler


def get_class_profiler(target_classes_dict, source_file, list_of_source_files, input_format,
                       instantiation_property_str, namespaces_to_ignore=None,
                       infer_numeric_types_for_untyped_literals=False,
                       raw_graph=None, namespaces_dict=None,
                       url_input=None, list_of_url_input=None,
                       shape_map_file=None,
                       shape_map_raw=None,
                       track_classes_for_entities_at_last_depth_level=True,
                       depth_for_building_subgraph=1,
                       url_endpoint=None,
                       strict_syntax_with_corners=False,
                       target_classes=None,
                       file_target_classes=None):
    yielder = get_triple_yielder(source_file=source_file,
                                 list_of_source_files=list_of_source_files,
                                 input_format=input_format,
                                 namespaces_to_ignore=namespaces_to_ignore,
                                 raw_graph=raw_graph,
                                 allow_untyped_numbers=infer_numeric_types_for_untyped_literals,
                                 namespaces_dict=namespaces_dict,
                                 url_input=url_input,
                                 list_of_url_input=list_of_url_input,
                                 shape_map_file=shape_map_file,
                                 shape_map_raw=shape_map_raw,
                                 track_classes_for_entities_at_last_depth_level=track_classes_for_entities_at_last_depth_level,
                                 depth_for_building_subgraph=depth_for_building_subgraph,
                                 url_endpoint=url_endpoint,
                                 instantiation_property=instantiation_property_str,
                                 strict_syntax_with_corners=strict_syntax_with_corners,
                                 target_classes=target_classes,
                                 file_target_classes=file_target_classes)

    return ClassProfiler(triples_yielder=yielder,
                         target_classes_dict=target_classes_dict,
                         instantiation_property_str=instantiation_property_str)
