from shexer.consts import NT, FIXED_SHAPE_MAP
from shexer.utils.factories.triple_yielders_factory import get_triple_yielder, tune_target_classes_if_needed, \
    read_target_classes_from_file
from shexer.core.instances.instance_tracker import InstanceTracker
from shexer.core.instances.mappings.shape_map_instance_tracker import ShapeMapInstanceTracker
from shexer.core.instances.mix.mixed_instance_tracker import MixedInstanceTracker
from shexer.utils.factories.iri_factory import create_IRIs_from_string_list
from shexer.utils.factories.shape_map_parser_factory import get_shape_map_parser
from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.model.graph.rdflib_sgraph import RdflibSgraph


def get_instance_tracker(instances_file_input=None, graph_file_input=None,
                         graph_list_of_files_input=None, target_classes=None,
                         file_target_classes=None, input_format=NT,
                         instantiation_property=None,
                         namespaces_to_ignore=None,
                         raw_graph=None,
                         all_classes_mode=False,
                         namespaces_dict=None,
                         url_input=None,
                         list_of_url_input=None,
                         shape_map_file=None,
                         shape_map_raw=None,
                         shape_map_format=FIXED_SHAPE_MAP,
                         track_classes_for_entities_at_last_depth_level=True,
                         depth_for_building_subgraph=1,
                         url_endpoint=None,
                         strict_syntax_with_corners=False
                         ):
    """

    :param instances_file_input:
    :param graph_file_input:
    :param graph_list_of_files_input:
    :param target_classes:
    :param file_target_classes:
    :param input_format:
    :param instantiation_property:
    :param namespaces_to_ignore:
    :param raw_graph:
    :param all_classes_mode:
    :param namespaces_dict:
    :param url_input:
    :param list_of_url_input:
    :param shape_map_file:
    :param shape_map_raw:
    :param track_classes_for_entities_at_last_depth_level:
    :param depth_for_building_subgraph:
    :param url_endpoint:
    :param strict_syntax_with_corners:
    :return:
    """

    instance_yielder = None
    if instances_file_input is not None:
        instance_yielder = get_triple_yielder(source_file=instances_file_input,
                                              input_format=input_format,
                                              namespaces_to_ignore=namespaces_to_ignore,
                                              raw_graph=raw_graph,
                                              namespaces_dict=namespaces_dict,
                                              url_input=url_input,
                                              list_of_url_input=list_of_url_input,
                                              instantiation_property=instantiation_property,
                                              shape_map_file=shape_map_file,
                                              shape_map_raw=shape_map_raw,
                                              track_classes_for_entities_at_last_depth_level=track_classes_for_entities_at_last_depth_level,
                                              depth_for_building_subgraph=depth_for_building_subgraph,
                                              url_endpoint=url_endpoint,
                                              strict_syntax_with_corners=strict_syntax_with_corners,
                                              target_classes=target_classes,
                                              file_target_classes=file_target_classes
                                              )
    else:
        instance_yielder = get_triple_yielder(source_file=graph_file_input,
                                              list_of_source_files=graph_list_of_files_input,
                                              input_format=input_format,
                                              namespaces_to_ignore=namespaces_to_ignore,
                                              raw_graph=raw_graph,
                                              namespaces_dict=namespaces_dict,
                                              url_input=url_input,
                                              list_of_url_input=list_of_url_input,
                                              instantiation_property=instantiation_property,
                                              shape_map_file=shape_map_file,
                                              shape_map_raw=shape_map_raw,
                                              track_classes_for_entities_at_last_depth_level=track_classes_for_entities_at_last_depth_level,
                                              depth_for_building_subgraph=depth_for_building_subgraph,
                                              url_endpoint=url_endpoint,
                                              strict_syntax_with_corners=strict_syntax_with_corners,
                                              target_classes=target_classes,
                                              file_target_classes=file_target_classes
                                              )

    selectors_tracker = None
    pure_instances_tracker = None

    if _are_there_selectors(shape_map_file, shape_map_raw):
        sgraph = _get_adequate_sgraph(endpoint_url=url_endpoint,
                                      raw_graph=raw_graph,
                                      graph_file_input=graph_file_input,
                                      url_input=url_input,
                                      graph_format=input_format)
        shape_map_parser = get_shape_map_parser(format=shape_map_format,
                                                sgraph=sgraph,
                                                namespaces_prefix_dict=namespaces_dict)
        selectors_tracker = ShapeMapInstanceTracker(shape_map=shape_map_parser.parse_shape_map(source_file=shape_map_file,
                                                                                               raw_content=shape_map_raw))
    if _are_there_some_target_classes(target_classes, file_target_classes, all_classes_mode):
        model_classes = None
        if not all_classes_mode:
            list_of_str_target_classes = tune_target_classes_if_needed(
                target_classes) if target_classes is not None else read_target_classes_from_file(file_target_classes)
            model_classes = get_list_of_model_classes(list_of_str_target_classes)

        pure_instances_tracker = InstanceTracker(target_classes=model_classes,
                                                 triples_yielder=instance_yielder,
                                                 instantiation_property=instantiation_property,
                                                 all_classes_mode=all_classes_mode,
                                                 track_hierarchies=False)

    return _decide_tracker_to_return(selectors_tracker, pure_instances_tracker)


def _get_adequate_sgraph(endpoint_url, graph_file_input, url_input, graph_format, raw_graph):
    if endpoint_url is not None:
        return EndpointSGraph(endpoint_url=endpoint_url)
    else:
        return RdflibSgraph(source_file=graph_file_input if graph_file_input is not None else url_input,
                            raw_graph=raw_graph,
                            format=graph_format)

def _decide_tracker_to_return(selectors_tracker, pure_instances_tracker):
    if selectors_tracker is not None and pure_instances_tracker is not None:
        return MixedInstanceTracker(list_of_instance_trackers=[selectors_tracker, pure_instances_tracker])
    return selectors_tracker if selectors_tracker is not None else pure_instances_tracker


def _are_there_selectors(shape_map_file, shape_map_raw):
    if shape_map_file is None and shape_map_raw is None:
        return False
    return True


def _are_there_some_target_classes(target_classes, file_target_classes, all_classes_mode):
    if target_classes is None and file_target_classes is None and not all_classes_mode:
        return False
    return True


def get_list_of_model_classes(list_of_str_target_classes):
    return create_IRIs_from_string_list(list_of_str_target_classes)



