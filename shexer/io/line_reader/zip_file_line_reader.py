class ZipFileLineReader(object):
    def __init__(self, zip_archive, zip_target):
        self._zip_archive = zip_archive
        self._zip_target = zip_target

    def read_lines(self):
        with self._zip_archive.open(self._zip_target, "r") as in_stream:
            for a_line in in_stream:
                yield a_line.decode("utf-8")

