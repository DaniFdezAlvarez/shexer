import gzip

class GzFileLineReader(object):

    def __init__(self, gz_file):
        self._gz_file = gz_file

    def read_lines(self):
        with gzip.open(self._gz_file, "r") as in_stream:
            for a_line in in_stream:
                yield a_line.decode("utf-8")
