from shexer.consts import RDF_TYPE

class SGraph(object):

    def __init__(self):
        pass

    def query_single_variable(self, str_query, variable_id):
        """
        It receives an SPARQL query with a single variable and returns a list with the nodes matching that query

        :param str_query:
        :param variable_id:
        :return: list
        """
        raise NotImplementedError()

    def yield_p_o_triples_of_an_s(self, target_node):
        """
        Here it expects unprefixed URIs. So there is no stage of namespaces management to build a query.

        :param target_node:
        :return:
        """
        raise NotImplementedError()

    def yield_s_p_triples_of_an_o(self, target_node):
        """
        Here it expects unprefixed URIs. So there is no stage of namespaces management to build a query.
        :param target_node:
        :return:
        """
        raise NotImplementedError()

    def yield_class_triples_of_an_s(self, target_node, instantiation_property):
        """
        Here it expects unprefixed URIs. So there is no stage of namespaces management to build a query.

        :param target_node:
        :param instantiation_property:
        :return:
        """
        raise NotImplementedError()

    def yield_s_p_triples_of_target_nodes(self, target_nodes, depth, classes_at_last_level=True,
                                          instantiation_property=RDF_TYPE, already_visited=None,
                                          strict_syntax_with_uri_corners=True
                                          ):
        """
        If it is provided, the param already_visited can be modified during the execution of this method.
        The set already_visited can be used to avoid repetition of triples calling this methodd repeatedly
        for different node selectors in a shape map.

        :param target_nodes:
        :param depth:
        :param classes_at_last_level:
        :param instantiation_property:
        :param already_visited:
        :param strict_syntax_with_uri_corners:
        :return:
        """
        current_already_visited = set() if already_visited is None else already_visited
        list_of_current_target_nodes = target_nodes
        new_target_nodes = []
        while depth > 0:
            for a_node in list_of_current_target_nodes:
                if a_node not in current_already_visited:
                    current_already_visited.add(a_node)
                    for a_triple in self.yield_s_p_triples_of_an_o(a_node):
                        yield a_triple
                        if self._is_an_unprefixed_iri(an_iri=a_triple[0],
                                                      strict_syntax_with_uri_corners=strict_syntax_with_uri_corners):
                            new_target_nodes.append(a_triple[0])
            depth -= 1
            list_of_current_target_nodes = new_target_nodes
            new_target_nodes = []
            if depth == 0 and classes_at_last_level:
                for a_node in list_of_current_target_nodes:
                    if a_node not in current_already_visited:
                        for a_triple in self.yield_class_triples_of_an_s(target_node=a_node,
                                                                         instantiation_property=instantiation_property):
                            yield a_triple

    def yield_p_o_triples_of_target_nodes(self, target_nodes, depth, classes_at_last_level=True,
                                          instantiation_property=RDF_TYPE, already_visited=None,
                                          strict_syntax_with_uri_corners=True):
        """
        If it is provided, the param already_visited can be modified during the execution of this method.
        The set already_visited can be used to avoid repetition of triples calling this methodd repeatedly
        for different node selectors in a shape map.

        :param target_nodes:
        :param depth:
        :param classes_at_last_level:
        :param instantiation_property:
        :param already_visited:
        :param strict_syntax_with_uri_corners:
        :return:
        """

        current_already_visited = set() if already_visited is None else already_visited
        list_of_current_target_nodes = target_nodes
        new_target_nodes = []
        while depth > 0:
            for a_node in list_of_current_target_nodes:
                if a_node not in current_already_visited:
                    current_already_visited.add(a_node)
                    for a_triple in self.yield_p_o_triples_of_an_s(a_node):
                        yield a_triple
                        if self._is_an_unprefixed_iri(an_iri=a_triple[2],
                                                      strict_syntax_with_uri_corners=strict_syntax_with_uri_corners):
                            new_target_nodes.append(a_triple[2])
            depth -= 1
            list_of_current_target_nodes = new_target_nodes
            new_target_nodes = []
            if depth == 0 and classes_at_last_level:
                for a_node in list_of_current_target_nodes:
                    if a_node not in current_already_visited:
                        for a_triple in self.yield_class_triples_of_an_s(target_node=a_node,
                                                                         instantiation_property=instantiation_property):
                            yield a_triple

    def yield_classes_with_instances(self, instantiation_property=RDF_TYPE):
        """
        It yields every class URI that has at least a declared instance
        :param instantiation_property:
        :return:
        """
        raise NotImplementedError()



    def _is_an_unprefixed_iri(self, an_iri, strict_syntax_with_uri_corners=True):
        if strict_syntax_with_uri_corners:
            return an_iri[0] == "<" and an_iri[-1] == ">"
        else:
            return an_iri.startswith("http://")  # Getting kicked in the chicken nuggets is worse than this decision
