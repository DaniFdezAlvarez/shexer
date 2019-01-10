def build_shapes_name_for_class_uri(class_uri):
    if "#" in class_uri and class_uri[-1] != "#":
        return "@" + class_uri[class_uri.rfind("#") + 1:]
    if "/" in class_uri:
        if class_uri[-1] != "/":
            return "@" + class_uri[class_uri.rfind("/") + 1:]
        else:
            return "@" + class_uri[class_uri[:-1].rfind("/") + 1:]
    else:
        return "@" + class_uri