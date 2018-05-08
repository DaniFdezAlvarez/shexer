
def _add_xsd_prefix(unprefixed_elem):
    return "xsd:" + unprefixed_elem


STRING_TYPE = _add_xsd_prefix("string")
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"

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
    if XSD_NAMESPACE in a_literal:
        substring = a_literal[a_literal.find("\"^^")]
        return substring[substring.find("#")+1:substring.find(" ")]
    else:
        raise RuntimeError("Unrecognized literal type:" + a_literal + ". Check whats happening before the big show")



def parse_literal(an_elem):
    # Expected: "2.09353678089e-08"^^<http://www.w3.org/2001/XMLSchema#float> .
    # Result: the actual float between '"', already converted to float
    content = an_elem[1:an_elem.find('"', 1)]
    elem_type = decide_literal_type(an_elem)







