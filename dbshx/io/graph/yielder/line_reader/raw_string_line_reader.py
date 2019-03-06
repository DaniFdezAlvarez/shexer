
class RawStringLineReader():

    def __init__(self, raw_string):
        self._raw_string = raw_string


    def read_lines(self):
        for a_line in self._raw_string.split("\n"):
            if a_line.strip() != "":
                yield a_line