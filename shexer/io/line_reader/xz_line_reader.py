from xz import open as xzopen


class XzFileLineReader(object):

    def __init__(self, xz_file):
        self._xz_file = xz_file

    def read_lines(self):
        with xzopen(self._xz_file, "r") as in_stream:
            for a_line in in_stream:
                yield a_line.decode("utf-8")