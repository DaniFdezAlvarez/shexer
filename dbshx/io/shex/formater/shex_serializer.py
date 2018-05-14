_SPACES_GAP_FOR_FREQUENCY = "          "
_SPACES_GAP_BETWEEN_TOKENS = "  "
_TARGET_LINE_LENGHT = 80
_SPACES_LEVEL_INDENTATION = "   "


class ShexSerializer(object):

    def __init__(self, target_file, shapes_list, aceptance_threshold=0.4):
        self._target_file = target_file
        self._shapes_list = shapes_list
        self._aceptance_theshold = aceptance_threshold
        self._lines_buffer = []


    def serialize_shex(self):

        for a_shape in self._shapes_list:
            self._serialize_shape(a_shape)
        self._flush()


    def _serialize_shape(self, a_shape):
        self._serialize_shape_name(a_shape)
        self._serialize_opening_of_rules()
        self._serialize_shape_rules(a_shape)
        self._serialize_closure_of_rule()
        self._serialize_shape_gap()


    def _flush(self):
        print "Flush! ========"
        self._write_lines_buffer()


    def _write_line(self, a_line, indent_level=0):
        print "--------", a_line
        self._lines_buffer.append(self._indentation_spaces(indent_level) + a_line + "\n")
        if len(self._lines_buffer) >= 5000:
            self._write_lines_buffer()
            self._lines_buffer = []


    def _write_lines_buffer(self):
        print "Me piden que escriba -----------------", len(self._lines_buffer)
        with open(self._target_file, "a") as out_stream:
            for a_line in self._lines_buffer:
                out_stream.write(a_line)


    def _indentation_spaces(self, indent_level):
        result = ""
        for i in range(0, indent_level):
            result += _SPACES_LEVEL_INDENTATION
        return result


    def _serialize_shape_rules(self, a_shape):
        # statements = []
        # for a_statement in a_shape.yield_statements():
        #     statements.append(a_statement)
        statements = [a_statement for a_statement in a_shape.yield_statements()]
        if len(statements) == 0 or statements[0].probability < self._aceptance_theshold:
            return
        last_valid_statement = False
        for i in range(0, len(statements)):
            if last_valid_statement:
                break
            if i == len(statements) - 1 or statements[i + 1].probability < self._aceptance_theshold:
                last_valid_statement = True
            self._serialize_statement(statements[i], last_valid_statement)


    def _serialize_statement(self, a_statement, is_last_statement_of_shape):
        result = a_statement.st_property + _SPACES_GAP_BETWEEN_TOKENS + a_statement.st_type + _SPACES_GAP_BETWEEN_TOKENS + self._cardinality_representation(
            a_statement.cardinality) + self._closure_of_statement(is_last_statement_of_shape)
        result += self._adequate_amount_of_final_spaces(result)
        result += self._probability_representation(a_statement.probability)
        self._write_line(result, indent_level=1)


    def _probability_representation(self, probability):
        return str(probability * 100) + " %"


    def _cardinality_representation(self, cardinality):
        if cardinality == "1" or cardinality == 1:
            return ""
        return str(cardinality)


    def _closure_of_statement(self, is_last_statement):
        if is_last_statement:
            return ""
        return ";"


    def _adequate_amount_of_final_spaces(self, current_line):
        if len(current_line) > _TARGET_LINE_LENGHT - 10:
            return _SPACES_GAP_FOR_FREQUENCY
        result = ""
        for i in range(0, _TARGET_LINE_LENGHT - len(current_line)):
            result += " "
        return result


    def _serialize_shape_name(self, a_shape):
        self._write_line(a_shape.name.replace("@", ":"))


    def _serialize_opening_of_rules(self):
        self._write_line("{")


    def _serialize_closure_of_rule(self):
        self._write_line("}")


    def _serialize_shape_gap(self):
        self._write_line("")
        self._write_line("")
