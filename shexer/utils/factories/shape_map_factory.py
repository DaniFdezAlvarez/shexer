from shexer.utils.factories.triple_yielders_factory import produce_shape_map_according_to_input
from shexer.model.graph.rdflib_sgraph import RdflibSgraph


def get_shape_map_if_needed(sm_format, remote_sgraph, namespaces_prefix_dict, target_classes,
                            file_target_classes, shape_map_file, shape_map_raw,
                            instantiation_property, shape_map_already_built=None,
                            rdflib_graph=None, raw_graph=None, source_file_graph=None, input_format=None,
                            limit_remote_instances=-1):
    if shape_map_file is None and shape_map_raw is None:
        return None
    if shape_map_already_built:
        return shape_map_already_built

    sgraph = remote_sgraph if remote_sgraph is not None else RdflibSgraph(rdflib_graph=rdflib_graph,
                                                                          raw_graph=raw_graph,
                                                                          source_file=source_file_graph,
                                                                          format=input_format)

    return produce_shape_map_according_to_input(sm_format=sm_format,
                                                sgraph=sgraph,
                                                namespaces_prefix_dict=namespaces_prefix_dict,
                                                target_classes=target_classes,
                                                file_target_classes=file_target_classes,
                                                shape_map_file=shape_map_file,
                                                shape_map_raw=shape_map_raw,
                                                instantiation_property=instantiation_property,
                                                shape_map_already_built=shape_map_already_built,
                                                limit_remote_instances=limit_remote_instances)