from shexer.io.graph.yielder.multi_nt_triples_yielder import MultiNtTriplesYielder
from shexer.io.graph.yielder.nt_triples_yielder import NtTriplesYielder
from shexer.io.graph.yielder.tsv_nt_triples_yielder import TsvNtTriplesYielder
from shexer.io.graph.yielder.multi_tsv_nt_triples_yielder import MultiTsvNtTriplesYielder
from shexer.io.graph.yielder.rdflib_triple_yielder import RdflibParserTripleYielder, RdflibTripleYielder
from shexer.io.graph.yielder.multi_rdflib_triple_yielder import MultiRdfLibTripleYielder
from shexer.io.graph.yielder.remote.sgraph_from_selectors_triple_yielder import SgraphFromSelectorsTripleYielder
from shexer.io.graph.yielder.filter.filter_namespaces_triple_yielder import FilterNamespacesTriplesYielder
from shexer.utils.factories.shape_map_parser_factory import get_shape_map_parser
from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.utils.translators.list_of_classes_to_shape_map import ListOfClassesToShapeMap
from shexer.utils.uri import remove_corners, unprefixize_uri_if_possible
from shexer.utils.dict import reverse_keys_and_values

from shexer.consts import NT, TSV_SPO, N3, TURTLE, RDF_XML, FIXED_SHAPE_MAP, JSON_LD


def produce_shape_map_according_to_input(sm_format, sgraph, namespaces_prefix_dict, target_classes,
                                         file_target_classes, shape_map_file, shape_map_raw,
                                         instantiation_property, shape_map_already_built=None,
                                         limit_remote_instances=-1):
    if shape_map_already_built is not None:
        return shape_map_already_built
    prefix_namespaces_dict = reverse_keys_and_values(namespaces_prefix_dict)
    if shape_map_raw is not None or shape_map_file is not None:
        shape_map_parser = get_shape_map_parser(format=sm_format,
                                                sgraph=sgraph,
                                                namespaces_prefix_dict=namespaces_prefix_dict)

        return shape_map_parser.parse_shape_map(source_file=shape_map_file,
                                                raw_content=shape_map_raw)
    else:
        translator = ListOfClassesToShapeMap(sgraph=sgraph,
                                             prefix_namespaces_dict=prefix_namespaces_dict)
        target_classes = tune_target_classes_if_needed(list_target_classes=target_classes,
                                                       prefix_namespaces_dict=prefix_namespaces_dict) \
            if target_classes is not None \
            else read_target_classes_from_file(file_target_classes=file_target_classes,
                                               prefix_namespaces_dict=prefix_namespaces_dict)
        return translator.str_class_list_to_shape_map_sparql_selectors(str_list=target_classes,
                                                                       instantiation_property=instantiation_property,
                                                                       limit_remote_instances=limit_remote_instances)

def get_triple_yielder(source_file=None, list_of_source_files=None, input_format=NT, namespaces_to_ignore=None,
                       allow_untyped_numbers=False, raw_graph=None, namespaces_dict=None, url_input=None,
                       list_of_url_input=None, rdflib_graph=None, shape_map_file=None, shape_map_raw=None, shape_map_format=FIXED_SHAPE_MAP,
                       track_classes_for_entities_at_last_depth_level=True, depth_for_building_subgraph=1,
                       url_endpoint=None, instantiation_property=None, strict_syntax_with_corners=False,
                       target_classes=None, file_target_classes=None, built_remote_graph=None,
                       built_shape_map=None, limit_remote_instances=-1):
    result = None
    if url_endpoint is not None:
        sgrpah = built_remote_graph if built_remote_graph is not None else EndpointSGraph(endpoint_url=url_endpoint)

        shape_map = built_shape_map
        if built_shape_map is None:
            shape_map = produce_shape_map_according_to_input(sm_format=shape_map_format,
                                                             sgraph=sgrpah,
                                                             namespaces_prefix_dict=namespaces_dict,
                                                             target_classes=target_classes,
                                                             file_target_classes=file_target_classes,
                                                             shape_map_file=shape_map_file,
                                                             shape_map_raw=shape_map_raw,
                                                             instantiation_property=instantiation_property,
                                                             limit_remote_instances=limit_remote_instances)
        result = SgraphFromSelectorsTripleYielder(shape_map=shape_map,
                                                  depth=depth_for_building_subgraph,
                                                  classes_at_last_level=track_classes_for_entities_at_last_depth_level,
                                                  instantiation_property=instantiation_property,
                                                  strict_syntax_with_corners=strict_syntax_with_corners,
                                                  allow_untyped_numbers=allow_untyped_numbers
                                                  )
    elif url_input is not None or list_of_url_input is not None:  # Always use rdflib to parse remote graphs
        if url_input:
            result = RdflibParserTripleYielder(source=url_input,
                                               allow_untyped_numbers=allow_untyped_numbers,
                                               raw_graph=raw_graph,
                                               input_format=input_format,
                                               namespaces_dict=namespaces_dict)
        else:  # elif list_of_url_input:
            result = MultiRdfLibTripleYielder(list_of_files=list_of_url_input,
                                              allow_untyped_numbers=allow_untyped_numbers,
                                              input_format=input_format,
                                              namespaces_dict=namespaces_dict)
    elif rdflib_graph is not None:
        result = RdflibTripleYielder(rdflib_graph=rdflib_graph,
                                     namespaces_dict=namespaces_dict)
    elif input_format == NT:
        if source_file is not None or raw_graph is not None:
            result = NtTriplesYielder(source_file=source_file,
                                      allow_untyped_numbers=allow_untyped_numbers,
                                      raw_graph=raw_graph)
        else:
            result = MultiNtTriplesYielder(list_of_files=list_of_source_files,
                                           allow_untyped_numbers=allow_untyped_numbers)
    elif input_format == TSV_SPO:
        if source_file is not None or raw_graph is not None:
            result = TsvNtTriplesYielder(source_file=source_file,
                                         allow_untyped_numbers=allow_untyped_numbers,
                                         raw_graph=raw_graph)
        else:
            result = MultiTsvNtTriplesYielder(list_of_files=list_of_source_files,
                                              allow_untyped_numbers=allow_untyped_numbers)
    elif input_format in [TURTLE, N3, RDF_XML, JSON_LD]:
        if source_file is not None or raw_graph is not None:
            result = RdflibParserTripleYielder(source=source_file,
                                               allow_untyped_numbers=allow_untyped_numbers,
                                               raw_graph=raw_graph,
                                               input_format=input_format,
                                               namespaces_dict=namespaces_dict)
        else:
            result = MultiRdfLibTripleYielder(list_of_files=list_of_source_files,
                                              allow_untyped_numbers=allow_untyped_numbers,
                                              input_format=input_format,
                                              namespaces_dict=namespaces_dict)

    else:
        raise ValueError("Not supported format: " + input_format)

    if namespaces_to_ignore is None:
        return result
    else:
        return FilterNamespacesTriplesYielder(actual_triple_yielder=result,
                                              namespaces_to_ignore=namespaces_to_ignore)


def tune_target_classes_if_needed(list_target_classes, prefix_namespaces_dict):
    result = []
    for a_original_class in list_target_classes:
        if a_original_class.startswith("<"):
            result.append(remove_corners(a_uri=a_original_class))
        else:
            result.append(unprefixize_uri_if_possible(target_uri=a_original_class,
                                                      prefix_namespaces_dict=prefix_namespaces_dict))
    return result


def read_target_classes_from_file(file_target_classes, prefix_namespaces_dict):
    result = []
    with open(file_target_classes, "r") as in_stream:
        for a_line in in_stream:
            candidate = a_line.strip()
            if candidate != "":
                result.append(candidate)
    return tune_target_classes_if_needed(list_target_classes=result,
                                         prefix_namespaces_dict=prefix_namespaces_dict)