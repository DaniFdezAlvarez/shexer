from flask import Flask, request
from flask_cors import CORS
from dbshx.shaper import NT
from dbshx.shaper import Shaper
import json

################ CONFIG

PORT = 5002
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



################ SUPPORT FUNCTIONS

def _return_json_error_pool(error_pool):
    print error_pool
    result = '{"Errors" : ['
    result += '"' + error_pool[0] + '"'
    for i in range(1, len(error_pool)):
        result += ', "' + error_pool[i] + '"'
    result += "]}"
    return result


def _missing_param_error(param):
    return "Missing mandatory param: " + param


def _parse_target_classes(data, error_pool):
    print data[TARGET_CLASSES_PARAM], len(data[TARGET_CLASSES_PARAM])
    print "yol"
    if TARGET_CLASSES_PARAM not in data:
        print "uh"
        error_pool.append(_missing_param_error(TARGET_CLASSES_PARAM))
        return
    if type(data[TARGET_CLASSES_PARAM]) != list:
        print "ah"
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    if len(data[TARGET_CLASSES_PARAM]) == 0 or type(data[TARGET_CLASSES_PARAM][0]) != unicode:
        print "eh"
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    return [str(a_uri) for a_uri in data[TARGET_CLASSES_PARAM]]

def _parse_graph(data, error_pool):
    if TARGET_GRAPH_PARAM not in data:
        error_pool.append(_missing_param_error(TARGET_CLASSES_PARAM))
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
        if type(data[key]) == unicode:
            if data[key] in ["True", "False"]:
                result = bool(data[key])
            else:
                error_pool.append(key + " must be 'True' or 'False'. " + opt_message)
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
                 keep_less_specific, threshold):
    print "Aqui vengo yo, a llamar"
    shaper = Shaper(target_classes=target_classes,input_format=input_fotmat, instantiation_property=instantiation_prop,
                    infer_numeric_types_for_untyped_literals=infer_untyped_num,
                    discard_useless_constraints_with_positive_closure=discard_useles_constraints,
                    all_instances_are_compliant_mode=all_compliant,
                    keep_less_specific=keep_less_specific,
                    raw_graph=graph)
    return shaper.shex_graph(threshold)



################ WS

app = Flask(__name__)

@app.route('/shexer', methods=['POST'])
def shexer():
    error_pool = []
    try:
        data = json.loads(request.json)
        print data, "eyy"
        print "Aqui vengo yo, a llamar1"
        target_classes = _parse_target_classes(data, error_pool)
        print "Aqui vengo yo, a llamar2"
        graph = _parse_graph(data, error_pool)
        print "Aqui vengo yo, a llamar3"
        input_fotmat = _parse_input_format(data, error_pool)
        print "Aqui vengo yo, a llamar4"
        instantiation_prop = _parse_instantiation_prop(data, error_pool)
        print "Aqui vengo yo, a llamar5"
        infer_untyped_num = _parse_infer_untyped_num(data, error_pool)
        print "Aqui vengo yo, a llamar6"
        discard_useles_constraints = _parse_discard_useless(data, error_pool)
        print "Aqui vengo yo, a llamar7"
        all_compliant = _parse_all_compliant(data, error_pool)
        print "Aqui vengo yo, a llamar8"
        keep_less_specific = _parse_keep_less_specific(data, error_pool)
        print "Aqui vengo yo, a llamar9"
        threshold = _parse_threshold(data, error_pool)
        print "Aqui vengo yo, a llamar10"

        if len(error_pool) == 0:
            return _call_shaper(target_classes,
                                graph=graph,
                                input_fotmat=input_fotmat,
                                instantiation_prop=instantiation_prop,
                                infer_untyped_num=infer_untyped_num,
                                discard_useles_constraints=discard_useles_constraints,
                                all_compliant=all_compliant,
                                keep_less_specific=keep_less_specific,
                                threshold=threshold)
        else:
           return _return_json_error_pool(error_pool)

    except BaseException as e:
        error_pool.append(e.message)
        return _return_json_error_pool(error_pool)

CORS(app)
if __name__ == "__main__":
    app.run(port=PORT, host=HOST)