from dbshx.utils.factories.triple_yielders_factory import get_triple_yielder
from dbshx.core.class_profiler import ClassProfiler


def get_class_profiler(target_classes_dict, source_file, list_of_source_files, input_format,
                       instantiation_property_str, namespaces_to_ignore=None,
                       infer_numeric_types_for_untyped_literals=False,
                       raw_graph=None, namespaces_dict=None):
    yielder = get_triple_yielder(source_file=source_file,
                                 list_of_source_files=list_of_source_files,
                                 input_format=input_format,
                                 namespaces_to_ignore=namespaces_to_ignore,
                                 raw_graph=raw_graph,
                                 allow_untyped_numbers=infer_numeric_types_for_untyped_literals,
                                 namespaces_dict=namespaces_dict)

    return ClassProfiler(triples_yielder=yielder,
                         target_classes_dict=target_classes_dict,
                         instantiation_property_str=instantiation_property_str)

