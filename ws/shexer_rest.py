import traceback
from flask import Flask, request
from flask_cors import CORS
from shexer.consts import NT, RDF_TYPE
from shexer.shaper import Shaper
from shexer.utils.uri import remove_corners
import json
import sys

################ CONFIG

# PORT = 8080
HOST = "0.0.0.0"
MAX_LEN = 100000


################ Default namespace

default_namespaces = {"http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                      "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
                      "http://www.w3.org/2001/XMLSchema#": "xsd",
                      "http://www.w3.org/XML/1998/namespace/": "xml",
                      "http://www.w3.org/2002/07/owl#": "owl"
                      }


################ PARAM NAMES

TARGET_CLASSES_PARAM = "target_classes"
"""
List of strings: List of target classes to associate a shape with
"""

TARGET_GRAPH_PARAM = "raw_graph"
"""
String: RDF content to be analyzed
"""

INPUT_FORMAT_PARAM = "input_format"
"""
String: RDF syntax used. Ntriples is used by default Accepted values -->

"nt" (n-triples)
"turtle" (turtle)
"xml" (RDF/XML)
"n3" (n3)
"json-ld" (JSON LD)
"tsv_spo" (lines with subject predicate and object separated by tab '\\t' chars 
"""


INSTANTIATION_PROPERTY_PARAM = "instantiation_prop"
"""
String: property used to links an instance with its class. rdf:type by default.
"""


NAMESPACES_TO_IGNORE_PARAM = "ignore"
"""
List of Strings: List of namespaces whose properties should be ignored during the shexing process.
"""

INFER_NUMERIC_TYPES_PARAM = "infer_untyped_nums"
"""
Bool: default, True. If True, it tries to infer the numeric type (xsd:int, xsd:float..) of 
untyped numeric literals 
"""

DISCARD_USELESS_CONSTRAINTS_PARAM = "discard_useless_constraints"
"""
Bool: default, True. default, True. If True, it keeps just the most possible specific constraint w.r.t. cardinality 
"""

ALL_INSTANCES_COMPLIANT_PARAM = "all_compliant"
"""
Bool: default, True. default, True. If False, the shapes produced may not be compliant with all the entities considered
to build them. This is because it won't use Kleene closeres for any constraint. 
"""

KEEP_LESS_SPECIFIC_PARAM = "keep_less_specific"
"""
Bool: default, True. It prefers to use "+" closures rather than exact cardinalities in the triple constraints
"""

ACEPTANCE_THRESHOLD_PARAM = "threshold"
"""
Float: number in [0,1] that indicates the minimum proportion of entities that should have a given feature for this
to be accepted as a triple constraint in the produced shape.
"""

ALL_CLASSES_MODE_PARAM = "all_classes"
"""
Bool: default, False. If True, it generates a shape for every elements with at least an instance 
in the considered graph.
"""
SHAPE_MAP_PARAM = "shape_map"
"""
String: shape map to associate nodes with shapes. It uses the same syntax of validation shape maps. 
"""

REMOTE_GRAPH_PARAM = "graph_url"
"""
String: URL to retrieve an online raw graph.
"""

ENDPOINT_GRAPH_PARAM = "endpoint"
"""
String: URL of an SPARQL endpoint.
"""

NAMESPACES_PARAM = "prefixes"
"""
Dict. key are namespaces and values are prefixes. The pairs key value provided here will be used 
to parse the RDF content and t write the resulting shapes.
"""

QUERY_DEPTH_PARAM = "query_depth"
"""
Integer: default, 1. It indicates the depth to generate queries when targeting a SPARQL endpoint.
Currently it can be 1 or 2.
"""

DISABLE_COMMENTS_PARAM = "disable_comments"
"""
Bool: default, False. When set to True, the shapes do not include comment 
with ratio of entities compliant with a triple constraint
"""

QUALIFIER_NAMESPACES_PARAM = "namespaces_for_qualifiers"
"""
List. Default, None. When a list with elements is provided, the properties in the namespaces specified are considered
to be pointers to qualifier nodes.
"""

SHAPE_QUALIFIERS_MODE_PARAM = "shape_qualifiers_mode"
"""
Bool: default, False. When set to true, a shape is generated for those nodes detected as qualifiers according to
Wikidata data model and the properties pointing to them specified in QUALIFIER_NAMESPACES_PARAM
"""




################ SUPPORT FUNCTIONS


def _build_namespaces_dict(new_prefixes, defaults):
    """
    It merges the default list of namespaces with a

    :param new_prefixes:
    :param defaults:
    :return:
    """
    for a_key in new_prefixes:
        defaults[a_key] = new_prefixes[a_key]
    return defaults


def _jsonize_response(response):
    result = json.dumps({'result' : response})
    return result
    # result = {'result' : response}
    # return json.dumps(result)
    # return response


def _return_json_error_pool(error_pool):
    result = '{"Errors" : ['
    result += '"' + error_pool[0] + '"'
    for i in range(1, len(error_pool)):
        result += ', "' + error_pool[i] + '"'
    result += "]}"
    return _jsonize_response(result)


def _missing_param_error(param):
    return "Missing mandatory param: " + param


def _parse_endpoint_sparql(data, error_pool):
    if ENDPOINT_GRAPH_PARAM not in data:
        return None
    if type(data[ENDPOINT_GRAPH_PARAM]) != str:
        error_pool.append("You must provide a URL (string) in the field " + ENDPOINT_GRAPH_PARAM)
        return None
    return str(data[ENDPOINT_GRAPH_PARAM])


def _parse_remote_graph(data, error_pool):
    if REMOTE_GRAPH_PARAM not in data:
        return None
    if type(data[REMOTE_GRAPH_PARAM]) != str:
        error_pool.append("You must provide a URL (string) in the field " + REMOTE_GRAPH_PARAM)
        return None
    return str(data[REMOTE_GRAPH_PARAM])


def _parse_shape_map(data, error_pool):
    if SHAPE_MAP_PARAM not in data:
        return None
    if type(data[SHAPE_MAP_PARAM]) != str:
        error_pool.append("You must provide a string containing the shape map")
        return
    return str(data[SHAPE_MAP_PARAM])


def _parse_namespaces_to_ignore(data, error_pool):
    if NAMESPACES_TO_IGNORE_PARAM not in data:
        return None
    if type(data[NAMESPACES_TO_IGNORE_PARAM]) != list:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + NAMESPACES_TO_IGNORE_PARAM)
        return None
    if len(data[NAMESPACES_TO_IGNORE_PARAM]) == 0 or type(data[NAMESPACES_TO_IGNORE_PARAM][0]) != str:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + NAMESPACES_TO_IGNORE_PARAM)
        return
    return [str(a_uri) for a_uri in data[NAMESPACES_TO_IGNORE_PARAM]]


def _parse_namespaces_for_qualifiers(data, error_pool):
    if QUALIFIER_NAMESPACES_PARAM not in data:
        return None
    if type(data[QUALIFIER_NAMESPACES_PARAM]) != list:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + QUALIFIER_NAMESPACES_PARAM)
        return None
    if len(data[QUALIFIER_NAMESPACES_PARAM]) == 0 or type(data[QUALIFIER_NAMESPACES_PARAM][0]) != str:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + QUALIFIER_NAMESPACES_PARAM)
        return
    return [str(a_uri) for a_uri in data[QUALIFIER_NAMESPACES_PARAM]]



def _parse_namespaces(data, error_pool):
    if NAMESPACES_PARAM not in data:
        return {}
    if type(data[NAMESPACES_PARAM]) != dict:
        error_pool.append("You must provide a dict namespace_URI --> prefix  in " + NAMESPACES_PARAM)
        return {}
    if len(data[NAMESPACES_PARAM]) == 0:
        error_pool.append("You must provide a dict namespace_URI --> prefix  in " + NAMESPACES_PARAM)
        return {}
    result = {}
    for a_key in data[NAMESPACES_PARAM]:
        result[str(a_key)] = str(data[NAMESPACES_PARAM][a_key])
    return result


def _parse_target_classes(data, error_pool):
    if TARGET_CLASSES_PARAM not in data:
        return None
    if type(data[TARGET_CLASSES_PARAM]) != list:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    if len(data[TARGET_CLASSES_PARAM]) == 0 or type(data[TARGET_CLASSES_PARAM][0]) != str:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    return [str(a_uri) for a_uri in data[TARGET_CLASSES_PARAM]]


def _parse_graph(data, error_pool):
    if TARGET_GRAPH_PARAM not in data:
        return None
    if type(data[TARGET_GRAPH_PARAM]) != str:
        error_pool.append("You must provide a str containing an RDF graph ")
        return
    if len(data[TARGET_GRAPH_PARAM]) > MAX_LEN:
        error_pool.append("The size of the graphic is too big for this deployment. Introduce a graph using less than "
                          + str(MAX_LEN) + " chars")
        return
    return str(data[TARGET_GRAPH_PARAM])


def _parse_str_param(data, error_pool, key, default_value, opt_message=""):
    result = default_value
    if key in data:
        if type(data[key]) == str:
            result = data[key]
        else:
            error_pool.append(key + " must be a str. " + opt_message)
            return
    return result


def _parse_bool_param(data, error_pool, key, default_value, opt_message=""):
    result = default_value
    if key in data:
        if type(data[key]) == bool:
            result = data[key]
        else:
            error_pool.append(key + " must be 'true' or 'false'. " + opt_message)
            return

    return result


def _parse_input_format(data, error_pool):
    return _parse_str_param(data=data, error_pool=error_pool, key=INPUT_FORMAT_PARAM, default_value=NT)


def _parse_instantiation_prop(data, error_pool):
    candidate = _parse_str_param(data=data, error_pool=error_pool, key=INSTANTIATION_PROPERTY_PARAM,
                                 default_value=RDF_TYPE,
                                 opt_message="The default value is rdf:type")
    return remove_corners(a_uri=candidate,
                          raise_error_if_no_corners=False)


def _parse_infer_untyped_num(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=INFER_NUMERIC_TYPES_PARAM, default_value=True,
                             opt_message="The default value is True")


def _parse_discard_useless(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=DISCARD_USELESS_CONSTRAINTS_PARAM, default_value=True,
                             opt_message="The default value is True")


def _parse_all_compliant(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=ALL_INSTANCES_COMPLIANT_PARAM,
                             default_value=True,
                             opt_message="The default value is True")


def _parse_all_classes_mode(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=ALL_CLASSES_MODE_PARAM,
                             default_value=False,
                             opt_message="The default value is False")

def _parse_shape_qualifiers_mode(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=SHAPE_QUALIFIERS_MODE_PARAM,
                             default_value=False,
                             opt_message="The default value is False")

def _parse_disable_comments(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=DISABLE_COMMENTS_PARAM,
                             default_value=False,
                             opt_message="The default value is False")


def _parse_keep_less_specific(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=ALL_INSTANCES_COMPLIANT_PARAM,
                             default_value=True,
                             opt_message="The default value is True")


def _parse_threshold(data, error_pool):
    if ACEPTANCE_THRESHOLD_PARAM in data:
        try:
            result = float(data[ACEPTANCE_THRESHOLD_PARAM])
            if result < 0 or result > 1:
                raise ValueError()
            return result
        except BaseException as e:
            error_pool.append(ACEPTANCE_THRESHOLD_PARAM + " must contain a float number in [0,1]. The default value is 0.")
    return 0.0


def _parse_query_depth(data, error_pool):
    if QUERY_DEPTH_PARAM in data:
        try:
            result = int(data[QUERY_DEPTH_PARAM])
            if result > 2 or result < 1:
                raise ValueError()
            return result
        except BaseException as e:
            error_pool.append(QUERY_DEPTH_PARAM + " must contain a an integer (1 or 2). The default value is 1.")
    return 1



def _call_shaper(target_classes, graph, input_fotmat, instantiation_prop,
                 infer_untyped_num, discard_useles_constraints, all_compliant,
                 keep_less_specific, threshold, all_classes_mode, namespaces_dict,
                 namespaces_to_ignore, shape_map, remote_graph, endpoint_sparql,
                 query_depth, disable_comments, namespaces_for_qualifier_props,
                 shape_qualifiers_mode):
    shaper = Shaper(target_classes=target_classes,
                    input_format=input_fotmat,
                    instantiation_property=instantiation_prop,
                    infer_numeric_types_for_untyped_literals=infer_untyped_num,
                    discard_useless_constraints_with_positive_closure=discard_useles_constraints,
                    all_instances_are_compliant_mode=all_compliant,
                    keep_less_specific=keep_less_specific,
                    raw_graph=graph,
                    all_classes_mode=all_classes_mode,
                    namespaces_dict=namespaces_dict,
                    namespaces_to_ignore=namespaces_to_ignore,
                    shape_map_raw=shape_map,
                    url_graph_input=remote_graph,
                    url_endpoint=endpoint_sparql,
                    depth_for_building_subgraph=query_depth,
                    disable_comments=disable_comments,
                    namespaces_for_qualifier_props=namespaces_for_qualifier_props,
                    shape_qualifiers_mode=shape_qualifiers_mode,
                    wikidata_annotation=True
                    )
    result = shaper.shex_graph(acceptance_threshold=threshold, string_output=True)
    return _jsonize_response(result)


def _check_combination_error_input_data(data, error_pool):
    target_params = [TARGET_GRAPH_PARAM, REMOTE_GRAPH_PARAM, ENDPOINT_GRAPH_PARAM]
    counter = 0
    for elem in target_params:
        if elem in data:

            counter += 1
    if counter != 1:
        error_pool.append("You must provide exactly one of the following params: " + ", ".join(target_params) + ".")
        return True
    return False


def _check_combination_error_target_shapes(data, error_pool, all_classes_mode):
    target_params = [TARGET_CLASSES_PARAM, SHAPE_MAP_PARAM]
    counter = 0
    for elem in target_params:
        if elem in data:
            counter += 1
    if counter == 1:
        return False
    if counter == 0 and ALL_CLASSES_MODE_PARAM in data and all_classes_mode == True:
        return False
    error_pool.append("Yoy must provide exactly one of " + ", ".join(target_params) + " or set " + ALL_CLASSES_MODE_PARAM + " to True")
    return True

def _check_all_classes_mode_uncompatibility(data, error_pool, all_classes_mode):
    if all_classes_mode and ENDPOINT_GRAPH_PARAM in data and SHAPE_MAP_PARAM not in data:
        error_pool.append("If you use all classes mode with input via endpoint, you must provide a shape map as well "
                          "to let sheXer knows what part of the graph it should consider.")



################ WS

app = Flask(__name__)

@app.route('/shexer', methods=['POST'])
def shexer():
    error_pool = []
    try:
        data = request.json
        input_fotmat = _parse_input_format(data, error_pool)
        instantiation_prop = _parse_instantiation_prop(data, error_pool)
        infer_untyped_num = _parse_infer_untyped_num(data, error_pool)
        discard_useles_constraints = _parse_discard_useless(data, error_pool)
        all_compliant = _parse_all_compliant(data, error_pool)
        keep_less_specific = _parse_keep_less_specific(data, error_pool)
        threshold = _parse_threshold(data, error_pool)
        all_classes_mode = _parse_all_classes_mode(data, error_pool)
        namespaces_to_ignore = _parse_namespaces_to_ignore(data, error_pool)
        namespaces = _parse_namespaces(data, error_pool)
        query_depth = _parse_query_depth(data, error_pool)
        disable_comments = _parse_disable_comments(data, error_pool)

        shape_qualifiers_mode = _parse_shape_qualifiers_mode(data, error_pool)
        namespaces_for_qualifier_props = _parse_namespaces_for_qualifiers(data, error_pool)

        target_classes = None
        graph = None
        shape_map = None
        remote_graph = None
        endpoint_sparql = None

        err_input = _check_combination_error_input_data(data, error_pool)
        if not err_input:
            graph = _parse_graph(data, error_pool)
            remote_graph = _parse_remote_graph(data, error_pool)
            endpoint_sparql = _parse_endpoint_sparql(data, error_pool)

        err_target = _check_combination_error_target_shapes(data, error_pool, all_classes_mode)
        if not err_target:
            target_classes = _parse_target_classes(data, error_pool)
            shape_map = _parse_shape_map(data, error_pool)
            _check_all_classes_mode_uncompatibility(data, error_pool, all_classes_mode)

        # remote_graph = _parse_remote_graph(data, error_pool)
        # endpoint_sparql = _parse_endpoint_sparql(data, error_pool)

        if len(error_pool) == 0:
            #todo: Call shaper with the new params!
            return _call_shaper(target_classes=target_classes,
                                graph=graph,
                                input_fotmat=input_fotmat,
                                instantiation_prop=instantiation_prop,
                                infer_untyped_num=infer_untyped_num,
                                discard_useles_constraints=discard_useles_constraints,
                                all_compliant=all_compliant,
                                keep_less_specific=keep_less_specific,
                                threshold=threshold,
                                all_classes_mode=all_classes_mode,
                                namespaces_dict=_build_namespaces_dict(namespaces, default_namespaces),
                                endpoint_sparql=endpoint_sparql,
                                shape_map=shape_map,
                                remote_graph=remote_graph,
                                namespaces_to_ignore=namespaces_to_ignore,
                                query_depth=query_depth,
                                disable_comments=disable_comments,
                                namespaces_for_qualifier_props=namespaces_for_qualifier_props,
                                shape_qualifiers_mode=shape_qualifiers_mode
                                )


        else:
           return _return_json_error_pool(error_pool)

    except BaseException as e:
        traceback.print_exc()
        error_pool.append("Internal unexpected server error: " + str(e))
        return _return_json_error_pool(error_pool)

def run():
    port = 80 if len(sys.argv) < 2 else int(sys.argv[1])
    CORS(app)
    app.run(port=port, host=HOST, ssl_context='adhoc')

if __name__ == "__main__":
    run()
