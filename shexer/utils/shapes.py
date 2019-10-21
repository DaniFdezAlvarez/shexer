from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME

def build_shapes_name_for_class_uri(class_uri):
    if "#" in class_uri and class_uri[-1] != "#":
        return STARTING_CHAR_FOR_SHAPE_NAME + class_uri[class_uri.rfind("#") + 1:]
    if "/" in class_uri:
        if class_uri[-1] != "/":
            return STARTING_CHAR_FOR_SHAPE_NAME + class_uri[class_uri.rfind("/") + 1:]
        else:
            return STARTING_CHAR_FOR_SHAPE_NAME + class_uri[class_uri[:-1].rfind("/") + 1:]
    else:
        return class_uri