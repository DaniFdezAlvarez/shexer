from dbshx.model.IRI import IRI
from dbshx.model.property import Property
from dbshx.model.Literal import Literal
from dbshx.model.bnode import BNode
from dbshx.utils.uri import remove_corners, parse_literal, FLOAT_TYPE


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
            float(a_token)
            return Literal(content=a_token.strip(),
                           elem_type=FLOAT_TYPE)
        except:
            pass
    else:  # ???
        raise ValueError("Unrecognized type of token: " + a_token)


def tune_prop(a_token):
    return Property(remove_corners(a_token))
