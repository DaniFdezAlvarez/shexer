from shexer.model.IRI import IRI

def create_IRI_from_string(an_str):
    return IRI(content=an_str)


def create_IRIs_from_string_list(str_list):
    result = []
    for an_str in str_list:
        result.append(create_IRI_from_string(an_str))
    return result

