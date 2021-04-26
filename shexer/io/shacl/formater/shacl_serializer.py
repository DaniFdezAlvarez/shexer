from shexer.core.class_profiler import RDF_TYPE_STR
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME
from rdflib import Graph, Namespace, URIRef, RDF, BNode, XSD, Literal
from shexer.model.statement import POSITIVE_CLOSURE, KLEENE_CLOSURE, OPT_CARDINALITY
from shexer.utils.uri import XSD_NAMESPACE, LANG_STRING_TYPE
from shexer.model.const_elem_types import IRI_ELEM_TYPE, LITERAL_ELEM_TYPE, DOT_ELEM_TYPE, BNODE_ELEM_TYPE
from shexer.io.wikidata import wikidata_annotation
from wlighter import TURTLE_FORMAT

_EXPECTED_SHAPE_BEGINING = STARTING_CHAR_FOR_SHAPE_NAME + "<"
_EXPECTED_SHAPE_ENDING = ">"

_SHACL_NAMESPACE = "http://www.w3.org/ns/shacl#"

_SHACL_PRIORITY_PREFIXES = ["sh", "shacl", "sha"]

_R_SHACL_SHAPE_URI = URIRef(_SHACL_NAMESPACE + "NodeShape")
_R_SHACL_PROPERTY_SHAPE_URI = URIRef(_SHACL_NAMESPACE + "PropertyShape")

_R_SHACL_TARGET_CLASS_PROP = URIRef(_SHACL_NAMESPACE + "targetClass")
_R_SHACL_PATH_PROP = URIRef(_SHACL_NAMESPACE + "path")
_R_SHACL_MIN_COUNT_PROP = URIRef(_SHACL_NAMESPACE + "minCount")
_R_SHACL_MAX_COUNT_PROP = URIRef(_SHACL_NAMESPACE + "maxCount")

_R_SHACL_PROPERTY_PROP = URIRef(_SHACL_NAMESPACE + "property")

_R_SHACL_DATATYPE_PROP = URIRef(_SHACL_NAMESPACE + "dataType")
_R_SHACL_NODEKIND_PROP = URIRef(_SHACL_NAMESPACE + "nodeKind")
_R_SHACL_NODE_PROP = URIRef(_SHACL_NAMESPACE + "node")

_R_SHACL_IN_PROP = URIRef(_SHACL_NAMESPACE + "in")

_R_SHACL_NODEKIND_IRI = URIRef(_SHACL_NAMESPACE + "IRI")
_R_SHACL_NODEKIND_LITERAL = URIRef(_SHACL_NAMESPACE + "Literal")
_R_SHACL_NODEKIND_BNODE = URIRef(_SHACL_NAMESPACE + "BlankNode")
_R_SHACL_NODEKIND_DOT = None

_R_LANG_STRING = URIRef("http://www.w3.org/2000/01/rdf-schema#langString")

_INTEGER = "i"
_STRING = "s"

_MACRO_MAPPING = {IRI_ELEM_TYPE: _R_SHACL_NODEKIND_IRI,
                  LITERAL_ELEM_TYPE: _R_SHACL_NODEKIND_LITERAL,
                  DOT_ELEM_TYPE: _R_SHACL_NODEKIND_BNODE,
                  BNODE_ELEM_TYPE: _R_SHACL_NODEKIND_DOT}


class ShaclSerializer(object):

    def __init__(self, target_file, shapes_list, namespaces_dict=None, string_return=False,
                 instantiation_property_str=RDF_TYPE_STR, wikidata_annotation=False):
        self._target_file = target_file
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._shapes_list = shapes_list
        self._string_return = string_return
        self._instantiation_property_str = instantiation_property_str
        self._wikidata_annotation = wikidata_annotation

        self._g_shapes = Graph()

        # self._uri_dict = {}

    def serialize_shapes(self):
        self._add_namespaces()
        self._add_shapes()
        return self._produce_output()

    #################### NAMESPACES

    def _add_namespaces(self):
        self._add_param_namespaces()
        self._add_shacl_namespace_if_needed()

    def _add_param_namespaces(self):
        for a_namespace, a_prefix in self._namespaces_dict.items():
            self._add_namespace(prefix=a_prefix,
                                namespace_str=a_namespace)

    def _add_namespace(self, prefix, namespace_str):
        self._g_shapes.bind(prefix=prefix,
                            namespace=Namespace(namespace_str))

    def _add_shacl_namespace_if_needed(self):
        if _SHACL_NAMESPACE in self._namespaces_dict:  # shacl already included
            return
        curr_prefixes = self._namespaces_dict.values()
        for a_prefix in _SHACL_PRIORITY_PREFIXES:  # trying default prefixes
            if a_prefix not in curr_prefixes:
                self._add_shacl_namespace(a_prefix)
                return
        counter = 1  # going for random prefixes, no defs. available
        candidate_pref = _SHACL_PRIORITY_PREFIXES[0] + str(counter)
        while candidate_pref in curr_prefixes:
            counter += 1
            candidate_pref = _SHACL_PRIORITY_PREFIXES[0] + str(counter)
        self._add_shacl_namespace(candidate_pref)

    def _add_shacl_namespace(self, shacl_prefix):
        self._add_namespace(prefix=shacl_prefix,
                            namespace_str=_SHACL_NAMESPACE)
        self._namespaces_dict[_SHACL_NAMESPACE] = shacl_prefix

    #################### SHAPES

    def _add_shapes(self):
        for a_shape in self._shapes_list:
            self._add_shape(a_shape)

    def _add_shape(self, shape):
        r_shape_uri = self._generate_shape_uri(shape_name=shape.name)
        self._add_shape_uri(r_shape_uri=r_shape_uri)
        self._add_target_class(r_shape_uri=r_shape_uri,
                               shape=shape)
        self._add_shape_constraints(shape=shape,
                                    r_shape_uri=r_shape_uri)

    def _add_target_class(self, shape, r_shape_uri):
        if shape.class_uri is not None:
            self._add_triple(r_shape_uri,
                             _R_SHACL_TARGET_CLASS_PROP,
                             URIRef(shape.class_uri))  # TODO check if this is always an abs. URI, not sure

    def _add_shape_constraints(self, shape, r_shape_uri):
        for a_statement in shape.yield_statements():
            self._add_constraint(statement=a_statement,
                                 r_shape_uri=r_shape_uri)

    def _is_instantiation_property(self, str_property):
        return str_property == self._instantiation_property_str

    def _add_constraint(self, statement, r_shape_uri):
        if self._is_instantiation_property(statement.st_property):
            self._add_instantiation_constraint(statement=statement,
                                               r_shape_uri=r_shape_uri)
        else:
            self._add_regular_constraint(statement=statement,
                                         r_shape_uri=r_shape_uri)

    def _add_exactly_one_cardinality(self, r_constraint_node):
        self._add_min_occurs(r_constraint_node=r_constraint_node,
                             min_occurs=1)
        self._add_max_occurs(r_constraint_node=r_constraint_node,
                             max_occurs=1)

    def _add_in_instance(self, r_constraint_node, statement):
        target_node = self._generate_r_uri_for_str_uri(statement.st_type)
        list_seed_node = self._generate_bnode()
        self._add_triple(r_constraint_node, _R_SHACL_IN_PROP, list_seed_node)
        self._add_triple(list_seed_node, RDF.first, target_node)
        self._add_triple(list_seed_node, RDF.rest, RDF.nil)

    def _add_instantiation_constraint(self, statement, r_shape_uri):
        r_constraint_node = self._generate_bnode()
        self._add_bnode_property(r_shape_uri=r_shape_uri,
                                 r_constraint_node=r_constraint_node)
        self._add_path(statement=statement,
                       r_constraint_node=r_constraint_node)
        self._add_exactly_one_cardinality(r_constraint_node=r_constraint_node)
        self._add_in_instance(statement=statement,
                              r_constraint_node=r_constraint_node)

    def _add_regular_constraint(self, statement, r_shape_uri):
        r_constraint_node = self._generate_bnode()
        self._add_bnode_property(r_shape_uri=r_shape_uri,
                                 r_constraint_node=r_constraint_node)
        self._add_path(statement=statement,
                       r_constraint_node=r_constraint_node)
        self._add_node_type(statement=statement,
                            r_constraint_node=r_constraint_node)
        self._add_cardinality(statement=statement,
                              r_constraint_node=r_constraint_node)

    def _add_path(self, statement, r_constraint_node):
        r_property_uri = self._generate_r_uri_for_str_uri(statement.st_property)
        self._add_triple(r_constraint_node, _R_SHACL_PATH_PROP, r_property_uri)

    def _generate_r_uri_for_str_uri(self, property_str):
        if property_str.startswith("<") and property_str.endswith(">"):
            return URIRef(property_str[1:-1])
        elif property_str.startswith("http://"):
            return URIRef(property_str)
        raise ValueError("Check here:", property_str)

    def _is_a_shape(self, target_type):
        return target_type.startswith(STARTING_CHAR_FOR_SHAPE_NAME)

    def _is_literal(self, target_type):
        return target_type == LANG_STRING_TYPE or target_type.startswith(XSD_NAMESPACE)

    def _is_macro(self, target_type):
        return target_type in _MACRO_MAPPING

    def _add_dataType_literal(self, r_constraint_node, target_type):
        if target_type == LANG_STRING_TYPE:
            type_node = _R_LANG_STRING
        elif target_type.endswith("integer"):
            type_node = XSD.integer
        elif target_type.endswith("float"):
            type_node = XSD.float
        elif target_type.endswith("string"):
            type_node = XSD.string
        else:
            raise ValueError("Check here:" + target_type)
        self._add_triple(r_constraint_node,
                         _R_SHACL_DATATYPE_PROP,
                         type_node)

    def _add_node_shape(self, r_constraint_node, target_type):
        self._add_triple(r_constraint_node,
                         _R_SHACL_NODE_PROP,
                         self._generate_shape_uri(shape_name=target_type))

    def _add_nodeKind_macro(self, r_constraint_node, target_type):
        type_node = _MACRO_MAPPING[target_type]
        if type_node is not None:
            self._add_triple(r_constraint_node,
                             _R_SHACL_NODEKIND_PROP,
                             type_node)

    def _add_node_type(self, statement, r_constraint_node):
        #  sh:dataType for literal types
        #  sh:nodeKind for IRI or similar macros.
        #  sh:node for a shape
        if self._is_literal(statement.st_type):
            self._add_dataType_literal(r_constraint_node=r_constraint_node,
                                       target_type=statement.st_type)
        elif self._is_macro(statement.st_type):
            self._add_nodeKind_macro(r_constraint_node=r_constraint_node,
                                     target_type=statement.st_type)
        elif self._is_a_shape(statement.st_type):
            self._add_node_shape(r_constraint_node=r_constraint_node,
                                 target_type=statement.st_type)
        else:
            raise ValueError("Check here: ")


    def _min_occurs_from_cardinality(self, cardinality):
        if cardinality in [KLEENE_CLOSURE, OPT_CARDINALITY]:
            return None
        elif cardinality == POSITIVE_CLOSURE:
            return 1
        else:
            return cardinality

    def _max_occurs_from_cardinality(self, cardinality):
        if cardinality in [KLEENE_CLOSURE, POSITIVE_CLOSURE]:
            return None
        elif cardinality == OPT_CARDINALITY:
            return 1
        else:
            return cardinality

    def _generate_r_literal(self, value, l_type):
        return Literal(value, datatype=self._map_rdflib_datatype(l_type))

    def _map_rdflib_datatype(self, l_type):
        if l_type == _INTEGER:
            return XSD.integer
        elif l_type == _STRING:
            return XSD.string
        else:
            raise ValueError("Check here: " + l_type)

    def _add_min_occurs(self, r_constraint_node, min_occurs):
        self._add_triple(r_constraint_node,
                         _R_SHACL_MIN_COUNT_PROP,
                         self._generate_r_literal(value=min_occurs,
                                                  l_type=_INTEGER))

    def _add_max_occurs(self, r_constraint_node, max_occurs):
        self._add_triple(r_constraint_node,
                         _R_SHACL_MAX_COUNT_PROP,
                         self._generate_r_literal(value=max_occurs,
                                                  l_type=_INTEGER))

    def _add_cardinality(self, statement, r_constraint_node):
        min_occurs = self._min_occurs_from_cardinality(statement.cardinality)
        max_occurs = self._max_occurs_from_cardinality(statement.cardinality)
        if min_occurs is not None:
            self._add_min_occurs(r_constraint_node=r_constraint_node,
                                 min_occurs=min_occurs)
        if max_occurs is not None:
            self._add_max_occurs(r_constraint_node=r_constraint_node,
                                 max_occurs=max_occurs)

    def _add_bnode_property(self, r_shape_uri, r_constraint_node):
        self._add_triple(r_shape_uri, _R_SHACL_PROPERTY_PROP, r_constraint_node)
        self._add_triple(r_constraint_node, RDF.type, _R_SHACL_PROPERTY_SHAPE_URI)

    def _generate_shape_uri(self, shape_name):
        if shape_name.startswith(_EXPECTED_SHAPE_BEGINING) and shape_name.endswith(_EXPECTED_SHAPE_ENDING):
            return URIRef(shape_name[2:-1])  # Excluding  "@<"  and ">
        raise ValueError("Check here:", shape_name)

    def _add_shape_uri(self, r_shape_uri):
        self._add_triple(r_shape_uri, RDF.type, _R_SHACL_SHAPE_URI)

    def _add_triple(self, s, p, o):
        self._g_shapes.add((s, p, o))

    @staticmethod
    def _generate_bnode():
        return BNode()

    #################### OUTPUT

    def _produce_output(self):
        if self._wikidata_annotation:
            return self._produce_wikidata_annotation_output()
        # destination = None if self._string_return else self._target_file
        if self._string_return:
            return self._g_shapes.serialize(format="turtle").decode("utf-8")
        else:
            self._g_shapes.serialize(destination=self._target_file, format="turtle")


    def _produce_wikidata_annotation_output(self):
        result = self._g_shapes.serialize(format="turtle").decode("utf-8")
        result = wikidata_annotation(raw_input=result,
                                     string_return=self._string_return,
                                     out_file=self._target_file,
                                     format=TURTLE_FORMAT,
                                     rdfs_comments=False)
        if self._string_return:
            return result

