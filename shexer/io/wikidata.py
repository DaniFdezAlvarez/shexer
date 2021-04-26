from wlighter import WLighter


def wikidata_annotation(raw_input, string_return, out_file, format, rdfs_comments):
    wlig = WLighter(raw_input=raw_input,
                    format=format,
                    languages=["en"],
                    generate_rdfs_comments=rdfs_comments,
                    mode_column_aligned=True)
    result = wlig.annotate_all(out_file=out_file, string_return=string_return)
    if string_return:
        return result
