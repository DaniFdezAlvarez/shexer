from gzip import open as gzopen
from zipfile import ZipFile
from xz import open as xzopen


def get_content_xz_file(xz_path):
    with xzopen(xz_path, "r") as in_stream:
        return in_stream.read()


def get_content_gz_file(gz_path):
    with gzopen(gz_path, "r") as in_stream:
        return in_stream.read()


def yield_contents_zip_dir(zip_path):
    with ZipFile(zip_path, 'r') as zip:
        for a_file_path in zip.filelist:
            with zip.open(a_file_path) as in_file:
                yield in_file.read()

def get_content_zip_internal_file(base_archive, target_file):
    with base_archive.open(target_file, "r") as in_file:
        return in_file.read()

def list_of_zip_internal_files(zip_base_archive):
    return zip_base_archive.namelist()