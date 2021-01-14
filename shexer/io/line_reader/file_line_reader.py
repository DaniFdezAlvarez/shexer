

class FileLineReader(object):

    def __init__(self, source_file):
        self._source_file = source_file

    def read_lines(self):
        with open(self._source_file, "r", errors='ignore') as in_stream:
            for a_line in in_stream:
                yield a_line