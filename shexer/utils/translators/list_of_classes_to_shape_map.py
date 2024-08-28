from shexer.model.shape_map import ShapeMap, ShapeMapItem
from shexer.io.shape_map.node_selector.node_selector_parser import NodeSelectorParser


class ListOfClassesToShapeMap(object):

    def __init__(self, sgraph, prefix_namespaces_dict):
        self._sgraph = sgraph
        self._selector_parser = NodeSelectorParser(prefix_namespaces_dict=prefix_namespaces_dict,
                                                   sgraph=sgraph)

    def str_class_list_to_shape_map_sparql_selectors(self, str_list, instantiation_property, limit_remote_instances):
        result = ShapeMap()
        instantiation_property = str(instantiation_property)
        for str_class in str_list:
            raw_selector = self._get_raw_selector_to_catch_instances_of_class_uri(class_uri=str_class,
                                                                                  instantiation_property=instantiation_property,
                                                                                  limit_remote_instances=limit_remote_instances)
            result.add_item(ShapeMapItem(node_selector=self._get_node_selector_object_for_raw_selector(raw_selector),
                                         shape_label=self._get_shape_label_for_class_uri(str_class)))
        return result

    def model_class_list_to_shape_map_sparql_selectors(self, obj_list, instantiation_property, limit_remote_instances):
        return self.str_class_list_to_shape_map_sparql_selectors(str_list=[str(an_elem) for an_elem in obj_list],
                                                                 instantiation_property=instantiation_property,
                                                                 limit_remote_instances=limit_remote_instances)

    def _get_shape_label_for_class_uri(self, class_uri):
        if "#" in class_uri and class_uri[-1] != "#":
            return class_uri[class_uri.rfind("#") + 1:]
        if "/" in class_uri:
            if class_uri[-1] != "/":
                return class_uri[class_uri.rfind("/") + 1:]
            else:
                return class_uri[class_uri[:-1].rfind("/") + 1:]
        else:
            return class_uri

    def _get_raw_selector_to_catch_instances_of_class_uri(self, class_uri, instantiation_property, limit_remote_instances):
        return 'SPARQL "select ?s where {{ ?s <{prop}> <{class_uri}> . FILTER (!isBlank(?s)) }} {limit}"'.format(  # FILTER (!isBlank(?c))
            class_uri=class_uri,
            prop=instantiation_property,
            limit="" if limit_remote_instances < 0 else "LIMIT " + str(limit_remote_instances)
        )
        # return '{' + 'FOCUS <{prop}> <{class_uri}>'.format(class_uri=class_uri, prop=instantiation_property) + '}'

    def _get_node_selector_object_for_raw_selector(self, raw_selector):
        return self._selector_parser.parse_node_selector(raw_selector=raw_selector)


