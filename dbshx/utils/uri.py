
def _add_prefix(unprefixed_elem, prefix):
    return prefix + ":" + unprefixed_elem

XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"
XSD_PREFIX = "xsd"

RDF_SYNTAX_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDF_PREFIX = "rdf"

DT_NAMESPACE = "http://dbpedia.org/datatype/"
DT_PREFIX = "dt"

STRING_TYPE = _add_prefix("string", XSD_PREFIX)


def remove_corners(a_uri):
    if a_uri.startswith("<") and a_uri.endswith(">"):
        return a_uri[1:-1]
    else:
        raise RuntimeError("Wrong parameter of function: '" + a_uri + "'")


def decide_literal_type(a_literal):
    if "\"^^" not in a_literal:
        return STRING_TYPE
    if there_is_arroba_after_last_quotes(a_literal):
        return STRING_TYPE
    if "xsd:" in a_literal:
        return a_literal[a_literal.find("xsd:"):]
    if "rdf:" in a_literal:
        return a_literal[a_literal.find("rdf:"):]
    if "dt:" in a_literal:
        return a_literal[a_literal.find("dt:"):]
    if XSD_NAMESPACE in a_literal:
        substring = a_literal[a_literal.find("\"^^"):]
        return _add_prefix(substring[substring.rfind("#")+1:-1], XSD_PREFIX)
    if RDF_SYNTAX_NAMESPACE in a_literal:
        substring = a_literal[a_literal.find("\"^^")]
        return _add_prefix(substring[substring.rfind("#")+1:-1], RDF_PREFIX)
    if DT_NAMESPACE in a_literal:
        substring = a_literal[a_literal.find("\"^^")]
        return _add_prefix(substring[substring.rfind("#")+1:-1], DT_PREFIX)

    else:
        raise RuntimeError("Unrecognized literal type:" + a_literal + ". Check whats happening before the big show")


def there_is_arroba_after_last_quotes(target_str):
    if target_str.rfind("@") > target_str.rfind('"'):
        return True
    return False

def parse_literal(an_elem):
    content = an_elem[1:an_elem.find('"', 1)]
    elem_type = decide_literal_type(an_elem)
    return content, elem_type







