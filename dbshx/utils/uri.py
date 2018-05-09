
def _add_prefix(unprefixed_elem, prefix):
    return prefix + ":" + unprefixed_elem

XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"
XSD_PREFIX = "xsd"

RDF_SYNTAX_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDF_PREFIX = "rdf"

STRING_TYPE = _add_prefix("string", XSD_PREFIX)

def remove_corners(a_uri):
    if a_uri.startswith("<") and a_uri.endswith(">"):
        return a_uri[1:-1]
    else:
        raise RuntimeError("Wrong parameter of function: '" + a_uri + "'")


def decide_literal_type(a_literal):
    if "\"^^" not in a_literal:
        return STRING_TYPE
    if "xsd:" in a_literal:
        return a_literal[a_literal.find("xsd:"): a_literal.find(" ")]
    if "rdf:" in a_literal:
        return a_literal[a_literal.find("rdf:"): a_literal.find(" ")]
    if XSD_NAMESPACE in a_literal:
        substring = a_literal[a_literal.find("\"^^")]
        return _add_prefix(substring[substring.find("#")+1:substring.find(">")], XSD_PREFIX)
    if RDF_SYNTAX_NAMESPACE in a_literal:
        substring = a_literal[a_literal.find("\"^^")]
        return _add_prefix(substring[substring.find("#") + 1:substring.find(">")], RDF_PREFIX)
    else:
        raise RuntimeError("Unrecognized literal type:" + a_literal + ". Check whats happening before the big show")



def parse_literal(an_elem):
    content = an_elem[1:an_elem.find('"', 1)]
    elem_type = decide_literal_type(an_elem)
    return content, elem_type







