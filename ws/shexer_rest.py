import traceback
from flask import Flask, request
from flask_cors import CORS
from dbshx.shaper import NT
from dbshx.shaper import Shaper
import json

################ CONFIG

PORT = 5008
HOST = "0.0.0.0"
MAX_LEN = 100000


################ PARAM NAMES

TARGET_CLASSES_PARAM = "target_classes"
TARGET_GRAPH_PARAM = "graph"
INPUT_FORMAT_PARAM = "input_format"
INSTANTIATION_PROPERTY_PARAM = "instantiation_prop"
NAMESPACES_TO_IGNORE_PARAM = "ignore"
INFER_NUMERIC_TYPES_PARAM = "infer_untyped_nums"
DISCARD_USELESS_CONSTRAINTS_PARAM = "discard_useless_constraints"
ALL_INSTANCES_COMPLIANT_PARAM = "all_compliant"
KEEP_LESS_SPECIFIC_PARAM = "keep_less_specific"
ACEPTANCE_THRESHOLD_PARAM = "threshold"
ALL_CLASSES_MODE_PARAM = "all_classes"



################ SUPPORT FUNCTIONS

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


def _parse_target_classes(data, error_pool):
    if TARGET_CLASSES_PARAM not in data:
        error_pool.append(_missing_param_error(TARGET_CLASSES_PARAM))
        return
    if type(data[TARGET_CLASSES_PARAM]) != list:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    if len(data[TARGET_CLASSES_PARAM]) == 0 or type(data[TARGET_CLASSES_PARAM][0]) != unicode:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    return [str(a_uri) for a_uri in data[TARGET_CLASSES_PARAM]]


def _parse_graph(data, error_pool):
    if TARGET_GRAPH_PARAM not in data:
        error_pool.append(_missing_param_error(TARGET_GRAPH_PARAM))
        return
    if type(data[TARGET_GRAPH_PARAM]) != unicode:
        error_pool.append("You must provide a str containing an RDF graph ")
        return
    if len(data[TARGET_GRAPH_PARAM]) > MAX_LEN:
        error_pool.append("The size of the graph is too big for this deployment. Introduce a graph using less than "
                          + str(MAX_LEN) + " chars")
        return
    return str(data[TARGET_GRAPH_PARAM])


def _parse_str_param(data, error_pool, key, default_value, opt_message=""):
    result = default_value
    if key in data:
        if type(data[key]) == unicode:
            result = str(data[key])
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
    return _parse_str_param(data=data, error_pool=error_pool, key=INPUT_FORMAT_PARAM, default_value="NT")


def _parse_instantiation_prop(data, error_pool):
    return _parse_str_param(data=data, error_pool=error_pool, key=INSTANTIATION_PROPERTY_PARAM,
                            default_value=NT,
                            opt_message="The default value is rdf:type")


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


def _parse_keep_less_specific(data, error_pool):
    return _parse_bool_param(data=data, error_pool=error_pool, key=ALL_INSTANCES_COMPLIANT_PARAM,
                             default_value=True,
                             opt_message="The default value is True")


def _parse_threshold(data, error_pool):
    if ACEPTANCE_THRESHOLD_PARAM in data:
        try:
            result = float(data[ACEPTANCE_THRESHOLD_PARAM])
            return result
        except BaseException as e:
            error_pool.append(ACEPTANCE_THRESHOLD_PARAM + " must contain a float number in [0,1]. The default value is 0.")
    return 0.0



def _call_shaper(target_classes, graph, input_fotmat, instantiation_prop,
                 infer_untyped_num, discard_useles_constraints, all_compliant,
                 keep_less_specific, threshold, all_classes_mode, namespaces_dict):
    shaper = Shaper(target_classes=target_classes,
                    input_format=input_fotmat,
                    instantiation_property=instantiation_prop,
                    infer_numeric_types_for_untyped_literals=infer_untyped_num,
                    discard_useless_constraints_with_positive_closure=discard_useles_constraints,
                    all_instances_are_compliant_mode=all_compliant,
                    keep_less_specific=keep_less_specific,
                    raw_graph=graph,
                    all_classes_mode=all_classes_mode,
                    namespaces_dict=namespaces_dict)
    result = shaper.shex_graph(aceptance_threshold=threshold, string_output=True)
    return _jsonize_response(result)

################ Default namespace

default_namespaces = {"http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                      "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
                      "http://www.w3.org/2001/XMLSchema#": "xml",
                      "http://www.w3.org/XML/1998/namespace/": "xml",
                      "http://www.w3.org/2002/07/owl#" : "owl"
                      }


################ WS

app = Flask(__name__)

@app.route('/shexer', methods=['POST'])
def shexer():
    error_pool = []
    try:
        data = request.json
        graph = _parse_graph(data, error_pool)
        input_fotmat = _parse_input_format(data, error_pool)
        instantiation_prop = _parse_instantiation_prop(data, error_pool)
        infer_untyped_num = _parse_infer_untyped_num(data, error_pool)
        discard_useles_constraints = _parse_discard_useless(data, error_pool)
        all_compliant = _parse_all_compliant(data, error_pool)
        keep_less_specific = _parse_keep_less_specific(data, error_pool)
        threshold = _parse_threshold(data, error_pool)
        all_classes_mode = _parse_all_classes_mode(data, error_pool)
        target_classes = None if all_classes_mode else _parse_target_classes(data, error_pool)

        if len(error_pool) == 0:
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
                                namespaces_dict=default_namespaces)
        else:
           return _return_json_error_pool(error_pool)

    except BaseException as e:
        traceback.print_exc()
        error_pool.append(e.message)
        return _return_json_error_pool(error_pool)

CORS(app)
if __name__ == "__main__":
    app.run(port=PORT, host=HOST)