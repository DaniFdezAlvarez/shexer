
def load_whole_file_content(source_file):
    with open(source_file, "r") as in_stream:
        return in_stream.read()