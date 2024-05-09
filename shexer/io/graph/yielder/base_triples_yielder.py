
from shexer.io.line_reader.file_line_reader import FileLineReader
from shexer.io.line_reader.raw_string_line_reader import RawStringLineReader
from shexer.io.line_reader.gz_line_reader import GzFileLineReader
from shexer.io.line_reader.zip_file_line_reader import ZipFileLineReader
from shexer.io.line_reader.xz_line_reader import XzFileLineReader
from shexer.utils.obj_references import check_just_one_not_none
from shexer.consts import ZIP, GZ, XZ

class BaseTriplesYielder(object):

    def __init__(self):
        pass

    def _decide_line_reader(self, raw_graph, source_file,
                            compression_mode=None,
                            zip_base_archive=None):
        check_just_one_not_none((source_file, "source_file"),
                                (raw_graph, "raw_graph"))
        if raw_graph is not None:
            return RawStringLineReader(raw_string=raw_graph)
        elif compression_mode is None:
            return FileLineReader(source_file=source_file)
        elif compression_mode == GZ:
            return GzFileLineReader(gz_file=source_file)
        elif compression_mode == ZIP:
            return ZipFileLineReader(zip_archive=zip_base_archive,
                                     zip_target=source_file)
        elif compression_mode == XZ:
            return XzFileLineReader(xz_file=source_file)
        else:
            raise ValueError("Unsupported compression mode: {}".format(compression_mode))

    def yield_triples(self):
        raise NotImplementedError("Implement this method in derived classes")