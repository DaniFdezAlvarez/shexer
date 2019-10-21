from shexer.consts import JSON, FIXED_SHAPE_MAP
from shexer.io.shape_map.shape_map_parser import JsonShapeMapParser, FixedShapeMapParser

def get_shape_map_parser(format, sgraph, namespaces_prefix_dict):
    if format == JSON:
        return JsonShapeMapParser(sgraph=sgraph,
                                  namespaces_prefix_dict=namespaces_prefix_dict)
    elif format == FIXED_SHAPE_MAP:
        return FixedShapeMapParser(namespaces_prefix_dict=namespaces_prefix_dict,
                                   sgraph=sgraph)
    else:
        raise ValueError("ShapeMap format not recognized:" + format)
