
def check_just_one_not_none(value1, value2, ref_name_1, ref_name_2):
    if None in [value1, value2] and value1 != value2:
        return
    raise ValueError(error_message_for_non_compatible_references(ref_name_1, ref_name_2))


def error_message_for_non_compatible_references(name_ref_1, name_ref_2):
    return "You must provide one and only one of the following params: " + name_ref_1 + " or " + name_ref_2

