from dbshx.model.IRI import IRI
from dbshx.model.property import Property
from dbshx.model.Literal import Literal
from dbshx.model.bnode import BNode
from dbshx.utils.uri import remove_corners, parse_literal, FLOAT_TYPE, INTEGER_TYPE


def check_if_property_belongs_to_namespace_list(str_prop, namespaces):
    """
    It return True if the property balongs to some namespace directly, i.e.,
    without adding any hierarchical element before reaching the name of the property itself.
    Example:
    Property http:example.org/prop, namespace http:example.org/ ---> True
    Property http:example.org/properties/prop, namespace http:example.org/ ---> False
    :param str_prop:
    :param namespaces:
    :return:
    """
    for a_namespace in namespaces:
        if str_prop.startswith(a_namespace):
            if "/" not in str_prop[len(a_namespace):] and "#" not in str_prop[len(a_namespace):]:
                return True
    return False


def tune_subj(a_token):
    if a_token.startswith("<"):
        return IRI(remove_corners(a_token))
    elif a_token.startswith('"'):
        content, elem_type = parse_literal(a_token)
        return Literal(content=content,
                       elem_type=elem_type)
    elif a_token.startswith("_:"):
        return BNode(identifier=a_token[2:])
    elif a_token.strip() == "[]":
        return BNode(identifier=a_token)

    else:  # ???
        raise ValueError("Unrecognized type of token: " + a_token)


def tune_token(a_token, allow_untyped_numbers=False):
    if a_token.startswith("<"):
        return IRI(remove_corners(a_token))
    elif a_token.startswith('"'):
        content, elem_type = parse_literal(a_token)
        return Literal(content=content,
                       elem_type=elem_type)
    elif a_token.startswith("_:"):
        return BNode(identifier=a_token[2:])
    elif a_token.strip() == "[]":
        return BNode(identifier=a_token)
    if allow_untyped_numbers:
        try:
            candidate_float = float(a_token)
            if _is_integer(candidate_float):
                return Literal(content=a_token.strip(),
                               elem_type=INTEGER_TYPE)
            return Literal(content=a_token.strip(),
                           elem_type=FLOAT_TYPE)
        except:
            pass
    else:  # ???
        raise ValueError("Unrecognized type of token: " + a_token)


def _is_integer(float_number):
    if float_number % 1.0 == 0:
        return True
    return False

def tune_prop(a_token):
    return Property(remove_corners(a_token))
