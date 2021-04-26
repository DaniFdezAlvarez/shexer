
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"
XSD_PREFIX = "xsd"

RDF_SYNTAX_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDF_PREFIX = "rdf"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

DT_NAMESPACE = "http://dbpedia.org/datatype/"
DT_PREFIX = "dt"

OPENGIS_NAMESPACE = "http://www.opengis.net/ont/geosparql#"
OPENGIS_PREFIX = "geo"

LANG_STRING_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString"
STRING_TYPE = "http://www.w3.org/2001/XMLSchema#string"
FLOAT_TYPE = "http://www.w3.org/2001/XMLSchema#float"
INTEGER_TYPE = "http://www.w3.org/2001/XMLSchema#integer"


def _add_prefix(unprefixed_elem, prefix):
    return prefix + ":" + unprefixed_elem


def remove_corners(a_uri, raise_error_if_no_corners=True):
    if a_uri.startswith("<") and a_uri.endswith(">"):
        return a_uri[1:-1]
    if raise_error_if_no_corners:
        raise ValueError("Wrong parameter of function: '" + a_uri + "'")
    else:
        return a_uri


def add_corners(a_uri):
    return "<" + a_uri + ">"


def add_corners_if_it_is_an_uri(a_candidate_uri):
    if a_candidate_uri.startswith("http://") or a_candidate_uri.startswith("https://"):  # TODO, check this!
        return "<" + a_candidate_uri + ">"
    return a_candidate_uri


def decide_literal_type(a_literal):
    if there_is_arroba_after_last_quotes(a_literal):
        return LANG_STRING_TYPE
    elif "\"^^" not in a_literal:
        return STRING_TYPE
    elif "xsd:" in a_literal:
        return XSD_NAMESPACE + a_literal[a_literal.find("xsd:") + 4:]
    elif "rdf:" in a_literal:
        return RDF_SYNTAX_NAMESPACE + a_literal[a_literal.find("rdf:")+ 4:]
    elif "dt:" in a_literal:
        return DT_NAMESPACE + a_literal[a_literal.find("dt:")+ 3:]
    elif "geo:" in a_literal:
        return OPENGIS_NAMESPACE + a_literal[a_literal.find("geo:") + 4:]
    elif XSD_NAMESPACE in a_literal or RDF_SYNTAX_NAMESPACE in a_literal \
            or DT_NAMESPACE in a_literal or OPENGIS_NAMESPACE in a_literal:
        # substring = a_literal[a_literal.find("\"^^"):]
        # return _add_prefix(substring[substring.rfind("#")+1:-1], XSD_PREFIX)
        return a_literal[a_literal.find("\"^^")+4:-1]
    elif a_literal.strip().endswith(">"):
        return a_literal[a_literal.find("\"^^") + 4:-1]
    else:
        raise RuntimeError("Unrecognized literal type:" + a_literal)


def is_a_correct_uri(target_uri, prefix_namespace_dict):
    """
    TODO: Here I am assuming that there is no forbiden char ( " < > # % { } | \ ^ ~ [ ] ` )
    :param target_uri:
    :param prefix_namespace_dict:
    :return:
    """
    if target_uri[0] == "<" and target_uri[-1] == ">":
        return True
    for a_prefix in prefix_namespace_dict:
        if target_uri.startswith(a_prefix + ":"):
            return True
        return False


def there_is_arroba_after_last_quotes(target_str):
    if target_str.rfind("@") > target_str.rfind('"'):
        return True
    return False


def parse_literal(an_elem):
    content = an_elem[1:an_elem.find('"', 1)]
    elem_type = decide_literal_type(an_elem)
    return content, elem_type

def parse_unquoted_literal(an_elem):
    elem_type = decide_literal_type(an_elem)
    return an_elem, elem_type


def unprefixize_uri_if_possible(target_uri, prefix_namespaces_dict):
    for a_prefix in prefix_namespaces_dict:
        if target_uri.startswith(a_prefix+":"):
            return target_uri.replace(a_prefix+":", prefix_namespaces_dict[a_prefix])
    return target_uri


def prefixize_uri_if_possible(target_uri, namespaces_prefix_dict):
    best_match = None
    candidate_uri = remove_corners(target_uri)
    for a_namespace in namespaces_prefix_dict:  # Prefixed element (all literals are prefixed elements)
        if candidate_uri.startswith(a_namespace):
            if best_match is None or len(best_match) < len(a_namespace):
                best_match = a_namespace

    return target_uri if best_match is None else candidate_uri.replace(best_match, namespaces_prefix_dict[best_match] + ":")






