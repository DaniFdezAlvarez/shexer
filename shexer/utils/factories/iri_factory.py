from shexer.model.IRI import IRI
from shexer.utils.uri import remove_corners

def create_IRI_from_string(an_str):
    return IRI(content=an_str)


def create_IRIs_from_string_list(str_list):
    result = []
    for an_str in str_list:
        result.append(create_IRI_from_string(remove_corners(a_uri=an_str,
                                                            raise_error_if_no_corners=False)))
    return result

