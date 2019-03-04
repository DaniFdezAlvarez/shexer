from flask import Flask, request
from flask_cors import CORS


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
DISCARD_USELESS_CONSTRAINTS_PARAM = "discard_useles_constraints"
ALL_INSTANCES_COMPLIANT_PARAM = "all_compliant"
KEEP_LESS_SPECIFIC_PARAM = "keep_less_specific"
ACEPTANCE_THRESHOLD_PARAM = "threshold"



################ SUPPORT FUNCTIONS

def _return_json_error_pool(error_pool):
    result = '{"Errors" : ['
    result += '"' + error_pool[1] + '"'
    for i in range(1, len(error_pool)):
        result += ', "' + error_pool[i] + '"'
    result += "]}"
    return result


def _missing_param_error(param):
    return "Missing mandatory param: " + param


def _parse_target_classes(data, error_pool):
    if TARGET_CLASSES_PARAM not in data:
        error_pool.append(_missing_param_error(TARGET_CLASSES_PARAM))
        return
    if type(data[TARGET_CLASSES_PARAM]) != list:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    if len(data[TARGET_CLASSES_PARAM] == 0) or type(data[TARGET_CLASSES_PARAM][0]) != str:
        error_pool.append("You must provide a non-empty list of URIs (string) in " + TARGET_CLASSES_PARAM)
        return
    return data[TARGET_CLASSES_PARAM]

def _parse_graph(data, error_pool):
    if TARGET_GRAPH_PARAM not in data:
        error_pool.append(_missing_param_error(TARGET_CLASSES_PARAM))
        return
    if type(data[TARGET_GRAPH_PARAM]) != str:
        error_pool.append("You must provide a str containing an RDF graph ")
        return
    if len(data[TARGET_GRAPH_PARAM]) > MAX_LEN:
        error_pool.append("The size of the graph is too big for this deployment. Introduce a graph using less than "
                          + str(MAX_LEN) + " chars")
        return
    return data[TARGET_GRAPH_PARAM]



################ WS

app = Flask(__name__)

@app.route('shexer', methods=['POST'])
def shexer():
    error_pool = []
    try:
        data = request.json
        target_classes = _parse_target_classes(data, error_pool)
        graph = _parse_graph(data, error_pool)
        input_fotmat = _parse_input_format(data, error_pool)
        instantiation_prop = _parse_instantiation_prop(data, error_pool)
        infer_untyped_num = _parse_infer_untyped_num(data, error_pool)
        discard_useles_constraints = _parse_discard_useless(data, error_pool)
        all_compliant = _parse_all_compliant(data, error_pool)
        keep_less_specific = _parse_keep_less_specific(data, error_pool)
        threshold = _parse_threshold(data, error_pool)

        if len(error_pool) == 0:
            pass  # TODO
        else:
           return _return_json_error_pool(error_pool)

    except BaseException as e:
        error_pool.append(e.message)
        return _return_json_error_pool(error_pool)

CORS(app)
if __name__ == "__main__":
    app.run(port=PORT, host=HOST)