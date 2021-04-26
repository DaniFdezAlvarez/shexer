from shexer.core.class_profiler import RDF_TYPE_STR

from shexer.model.property import Property
from shexer.utils.uri import remove_corners
from shexer.utils.shapes import prefixize_shape_name_if_possible
from shexer.io.shex.formater.consts import SPACES_LEVEL_INDENTATION
from shexer.io.wikidata import wikidata_annotation
from shexer.io.file import read_file

from wlighter import SHEXC_FORMAT



class ShexSerializer(object):

    def __init__(self, target_file, shapes_list, namespaces_dict=None, string_return=False,
                 instantiation_property_str=RDF_TYPE_STR, disable_comments=False, wikidata_annotation=False):
        self._target_file = target_file
        self._shapes_list = shapes_list
        self._lines_buffer = []
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._string_return = string_return
        self._instantiation_property_str = self._decide_instantiation_property(instantiation_property_str)
        self._disable_comments = disable_comments
        self._wikidata_annotation = wikidata_annotation

        self._string_result = ""

    def serialize_shapes(self):

        self._reset_target_file()
        self._serialize_namespaces()
        for a_shape in self._shapes_list:
            self._serialize_shape(a_shape)
        self._flush()
        if self._wikidata_annotation:
            self._annotate_wikidata_ids_in_result()
        if self._string_return:
            return self._string_result

    @staticmethod
    def _decide_instantiation_property(instantiation_property_str):
        if instantiation_property_str == None:
            return RDF_TYPE_STR
        if type(instantiation_property_str) == Property:
            return str(instantiation_property_str)
        if type(instantiation_property_str) == str:
            return remove_corners(a_uri=instantiation_property_str,
                                  raise_error_if_no_corners=False)
        raise ValueError("Unrecognized param type to define instantiation property")

    def _annotate_wikidata_ids_in_result(self):
        self._string_result =  wikidata_annotation(raw_input=self._get_raw_input_for_wikidata_annotation(),
                                                   string_return=self._string_return,
                                                   out_file=self._target_file,
                                                   format=SHEXC_FORMAT,
                                                   rdfs_comments=True)

    def _get_raw_input_for_wikidata_annotation(self):
        if self._string_return:
            return self._string_result
        return read_file(self._target_file)


    def _serialize_namespaces(self):
        for a_namespace in self._namespaces_dict:
            self._write_line(self._prefix_line(a_namespace), 0)
        self._write_line("", 0)

    def _prefix_line(self, namespace_key):
        return "PREFIX " + self._namespaces_dict[namespace_key] + ": <" + namespace_key + ">"

    def _serialize_empty_namespace(self):
        self._write_line("PREFIX : <http://weso.es/shapes/>")

    def _serialize_shape(self, a_shape):
        self._serialize_shape_name(a_shape)
        self._serialize_opening_of_rules()
        self._serialize_shape_rules(a_shape)
        self._serialize_closure_of_rule()
        self._serialize_shape_gap()

    def _flush(self):
        self._write_lines_buffer()

    def _write_line(self, a_line, indent_level=0):
        self._lines_buffer.append(self._indentation_spaces(indent_level) + a_line + "\n")
        if len(self._lines_buffer) >= 5000:
            self._write_lines_buffer()
            self._lines_buffer = []

    def _reset_target_file(self):
        if self._string_return:
            return
        with open(self._target_file, "w") as out_stream:
            out_stream.write("")  # Is this necessary? maybe enough to open it in 'w' mode?

    def _write_lines_buffer(self):
        if self._string_return:
            self._string_result += "".join(self._lines_buffer)
        else:
            with open(self._target_file, "a") as out_stream:
                for a_line in self._lines_buffer:
                    out_stream.write(a_line)

    def _indentation_spaces(self, indent_level):
        result = ""
        for i in range(0, indent_level):
            result += SPACES_LEVEL_INDENTATION
        return result

    def _serialize_shape_rules(self, a_shape):
        if a_shape.n_statements == 0:
            return
        statements = a_shape.statements
        for i in range(0, len(statements) - 1):
            for line_indent_tuple in statements[i]. \
                    get_tuples_to_serialize_line_indent_level(is_last_statement_of_shape=False,
                                                              namespaces_dict=self._namespaces_dict):
                self._write_line(a_line=line_indent_tuple[0],
                                 indent_level=line_indent_tuple[1])
        for line_indent_tuple in statements[len(statements) - 1]. \
                get_tuples_to_serialize_line_indent_level(is_last_statement_of_shape=True,
                                                          namespaces_dict=self._namespaces_dict):
            self._write_line(a_line=line_indent_tuple[0],
                             indent_level=line_indent_tuple[1])

    def _serialize_shape_name(self, a_shape):
        self._write_line(
            prefixize_shape_name_if_possible(a_shape_name=a_shape.name,
                                             namespaces_prefix_dict=self._namespaces_dict)
        )

    def _serialize_opening_of_rules(self):
        self._write_line("{")

    def _serialize_closure_of_rule(self):
        self._write_line("}")

    def _serialize_shape_gap(self):
        self._write_line("")
        self._write_line("")
