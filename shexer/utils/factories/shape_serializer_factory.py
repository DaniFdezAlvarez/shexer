from shexer.consts import SHEX
from shexer.io.shex.formater.shex_serializer import ShexSerializer


def get_shape_serializer(output_format, shapes_list, target_file=None, string_return=False, namespaces_dict=None,
                         instantiation_property=None, disable_comments=False):
    if output_format == SHEX:
        return ShexSerializer(target_file=target_file,
                              shapes_list=shapes_list,
                              namespaces_dict=namespaces_dict,
                              string_return=string_return,
                              instantiation_property_str=instantiation_property,
                              disable_comments=disable_comments)
    else:
        raise ValueError("Currently unsupported format: " + output_format)
