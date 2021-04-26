from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff
import re

_BLANKS = re.compile("[ \t]+")
_LINE_JUMPS = re.compile("\n+")

_PREFIX = "PREFIX"
_BEG_SHAPE = "{"
_END_SHAPE = "}"
_BEG_OR = "("
_END_OR = ")"
_OR = "|"


def get_namespaces_and_shapes_from_str(str_target, or_shapes=False):
    if or_shapes:
        return get_namespaces_and_shapes_from_str_with_or(str_target)
    namespaces = []
    shapes = {}
    last_line = ""
    current_shape = None

    for a_line in str_target.split("\n"):
        if a_line.startswith(_PREFIX):
            namespaces.append(a_line)
        elif a_line.startswith(_BEG_SHAPE):
            current_shape = last_line
            shapes[last_line] = []
        elif a_line.startswith(_END_SHAPE):
            current_shape = None
        elif current_shape is not None:
            shapes[current_shape].append(a_line.replace(";", "").strip())  # Avoid trailing ";", that can be there or not

        last_line = a_line  # Always execute

    return namespaces, shapes

def get_namespaces_and_shapes_from_str_with_or(str_target):
    namespaces = []
    shapes = {}
    last_line = ""
    current_shape = None

    or_mode = False
    current_or = None

    for a_line in str_target.split("\n"):
        a_line = a_line.strip()
        if a_line.startswith(_PREFIX):
            namespaces.append(a_line)
        elif a_line.startswith(_BEG_SHAPE):
            current_shape = last_line
            shapes[last_line] = []
        elif a_line.startswith(_END_SHAPE):
            current_shape = None
        elif a_line.startswith(_BEG_OR):
            or_mode = True
            current_or = ""
        elif or_mode:
            if not a_line.startswith(_END_OR):
                current_or = current_or + a_line
            else:
                or_mode = False
                shapes[current_shape].append(current_or)

        elif current_shape is not None:
            shapes[current_shape].append(
                a_line.replace(";", "").strip())  # Avoid trailing ";", that can be there or not

        last_line = a_line  # Always execute

    return namespaces, shapes



def unordered_lists_match(list1, list2):
    return set(list1) == set(list2)

def unordered_sets_match(sets1, sets2):
    for a_set1 in sets1:
        if a_set1 not in sets2:
            return False
    return True

def simple_and_or_str_constraints(str_constraints):  # TODO Fix here. Receive a dict, not a list. check call to this method
    simple_c = []
    or_c = []
    for a_c in str_constraints:
        if _OR in a_c:
            or_c.append(a_c)
        else:
            simple_c.append(a_c)
    return simple_c, or_c

def unordered_or_constraints_match(or_list_1, or_list_2):
    if len(or_list_1) != len(or_list_2):
        return False
    for i in range(len(or_list_1)):
        or_list_1[i] = set(or_list_1[i].split(_OR))
        or_list_2[i] = set(or_list_2[i].split(_OR))
    return unordered_sets_match(or_list_1, or_list_2)


def or_shapes_comparison(shapes1, shapes2):
    for a_key_label in shapes1:
        if a_key_label not in shapes2:
            return False
        simple_constraints1, or_constraints1 = simple_and_or_str_constraints(shapes1[a_key_label])
        simple_constraints2, or_constraints2 = simple_and_or_str_constraints(shapes2[a_key_label])
        if not unordered_lists_match(simple_constraints1, simple_constraints2):
            return False
        if not unordered_or_constraints_match(or_constraints1, or_constraints2):
            return False
    return True


def namespaces_match(names1, names2):
    return unordered_lists_match(names1, names2)


def shapes_match(shapes1, shapes2, or_shapes=False):
    if len(shapes1) != len(shapes2):
        return False
    if or_shapes:
        return or_shapes_comparison(shapes1, shapes2)
    for a_key_label in shapes1:
        if a_key_label not in shapes2:
            return False
        if not unordered_lists_match(shapes1[a_key_label], shapes2[a_key_label]):
            return False
    return True


def complex_shape_comparison(str1, str2, or_shapes=False):
    namespaces1, shapes1 = get_namespaces_and_shapes_from_str(str1, or_shapes)
    namespaces2, shapes2 = get_namespaces_and_shapes_from_str(str2, or_shapes)

    if not namespaces_match(namespaces1, namespaces2):
        return False
    return shapes_match(shapes1, shapes2, or_shapes)


def normalize_str(str_target):
    result = str_target.strip()
    result = _BLANKS.sub(result, " ")
    return _LINE_JUMPS.sub(result, "\n")


def tunned_str_comparison(str1, str2, or_shapes=False):
    if normalize_str(str1) == normalize_str(str2):
        return True
    else:
        return complex_shape_comparison(str1, str2, or_shapes)

def file_vs_str_tunned_comparison(file_path, str_target, or_shapes=False):
    with open(file_path, "r") as in_stream:
        content = in_stream.read()
    return tunned_str_comparison(content, str_target, or_shapes)

def file_vs_str_exact_comparison(file_path, target_str):
    with open(file_path, "r") as in_stream:
        return in_stream.read().strip() == target_str.strip()

def file_vs_file_tunned_comparison(file_path1, file_path2, or_shapes=False):
    with open(file_path1, "r") as in_stream:
        content1 = in_stream.read()
    with open(file_path2, "r") as in_stream:
        content2 = in_stream.read()
    return tunned_str_comparison(content1, content2, or_shapes)

def number_of_shapes(target_str):
    counter = 0
    for a_line in target_str.split("\n"):
        if a_line.startswith(_BEG_SHAPE):
            counter += 1
    return counter

def shape_contains_constraint(target_str, shape, constraint):
    constraint = constraint.replace(";","").strip()
    lines = target_str.split("\n")
    seeking_mode = False
    for i in range(len(lines)):
        if seeking_mode:
            if lines[i].replace(";", "").strip() == constraint:
                return True
            if lines[i].startswith(_END_SHAPE):
                return False
        if lines[i].startswith(_BEG_SHAPE) and shape == lines[i-1].strip():
            seeking_mode = True
    return False


def graph_comparison_rdflib(g1, g2):
    iso1 = to_isomorphic(g1)
    iso2 = to_isomorphic(g2)
    both, in1, in2 = graph_diff(iso1, iso2)
    return len(both) == len(g1) and len(in1) == 0 and len(in2) == 0


def graph_comparison_file_vs_str(file_path, str_target, format="turtle"):
    g1 = Graph()
    g1.parse(data=str_target, format=format)

    g2 = Graph()
    g2.parse(source=file_path, format=format)

    return graph_comparison_rdflib(g1, g2)

def text_contains_lines(text, list_lines):
    for a_line in list_lines:
        if a_line not in text:
            print(a_line)
            return False
        return True

