from shexer.consts import SHEXC, SHACL_TURTLE
from shexer.io.shex.formater.shex_serializer import ShexSerializer
from shexer.io.shacl.formater.shacl_serializer import ShaclSerializer


def get_shape_serializer(output_format, shapes_list, target_file=None, string_return=False, namespaces_dict=None,
                         instantiation_property=None, disable_comments=False, wikidata_annotation=False):
    if output_format == SHEXC:
        return ShexSerializer(target_file=target_file,
                              shapes_list=shapes_list,
                              namespaces_dict=namespaces_dict,
                              string_return=string_return,
                              instantiation_property_str=instantiation_property,
                              disable_comments=disable_comments,
                              wikidata_annotation=wikidata_annotation)
    elif output_format == SHACL_TURTLE:
        return ShaclSerializer(target_file=target_file,
                               shapes_list=shapes_list,
                               namespaces_dict=namespaces_dict,
                               string_return=string_return,
                               instantiation_property_str=instantiation_property,
                               wikidata_annotation=wikidata_annotation)
    else:
        raise ValueError("Currently unsupported format: " + output_format)
