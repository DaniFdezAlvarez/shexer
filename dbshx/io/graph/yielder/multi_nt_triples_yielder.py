
from dbshx.utils.log import log_to_error
from dbshx.utils.uri import remove_corners, parse_literal, there_is_arroba_after_last_quotes
from dbshx.model.IRI import IRI
from dbshx.model.literal import Literal
from dbshx.model.bnode import BNode
from dbshx.model.property import Property



class MultiNtTriplesYielder(object):
    def __init__(self, list_of_files):
        self._list_of_files = list_of_files
        self._triples_count = 0
        self._error_triples = 0



    def yield_triples(self):
        self._reset_count()
        for a_source_file in self._list_of_files:
            print "New file! --> ", a_source_file
            for a_triple in self._yield_triples_of_file(a_source_file):
                yield a_triple

    def _yield_triples_of_file(self, a_source_file):
        with open(a_source_file, "r") as in_stream:
            for a_line in in_stream:
                tokens = self._look_for_tokens(a_line.strip())
                if len(tokens) != 3:
                    self._error_triples += 1
                    log_to_error(msg="This line caused error: " + a_line,
                                 source=a_source_file)
                else:
                    yield (self._tune_token(tokens[0]), self._tune_prop(tokens[1]), self._tune_token(tokens[2]))
                    self._triples_count += 1
                    # if self._triples_count % 1000000 == 0:
                    #     print "Reading...", self._triples_count


    def _look_for_tokens(self, str_line):
        result = []
        current_first_index = 0
        while current_first_index != len(str_line):
            if str_line[current_first_index] == "<":
                last_index = self._look_for_last_index_of_uri_token(str_line, current_first_index)
                result.append(str_line[current_first_index:last_index+1])
                current_first_index = last_index +1
            elif str_line[current_first_index] == '"':
                last_index = self._look_for_last_index_of_literal_token(str_line, current_first_index)
                result.append(str_line[current_first_index:last_index + 1])
                print str_line[current_first_index:last_index + 1]
                current_first_index = last_index + 1
            elif str_line[current_first_index] == '.':

                break
            else:
                current_first_index += 1

        return result

    def _look_for_last_index_of_uri_token(self, target_str, first_index):
        target_substring = target_str[first_index:]
        index_sub = target_substring.find(">")
        return index_sub + (len(target_str) - len(target_substring))

    def _look_for_last_index_of_literal_token(self, target_str, first_index):
        target_substring = target_str[first_index:]

        if there_is_arroba_after_last_quotes(target_substring):  # String labelled with language
            return target_substring[target_substring.rfind("@"):].find(" ") - 1 + target_str.rfind("@")
        elif "^^" not in target_substring:  # Not typed
            success = False
            index_of_quotes = 1
            while not success:
                index_of_second_quotes = target_substring[index_of_quotes+1:].find('"') + index_of_quotes + 1
                if target_substring[index_of_second_quotes-1] != "\\":
                    success = True
                elif target_substring[index_of_second_quotes-2] == "\\":  # Case of escaped slash "\\"
                    success = True
                index_of_quotes = index_of_second_quotes
            return index_of_quotes + (len(target_str) - len(target_substring))
        else:  # Typed
            return target_substring[target_substring.find("^^"):].find(" ") - 1 + target_str.find("^^")


    def _tune_token(self, a_token):
        if a_token.startswith("<"):
            return IRI(remove_corners(a_token))
        elif a_token.startswith('"'):
            content, elem_type = parse_literal(a_token)
            return Literal(content=content,
                           elem_type=elem_type)
        else:  # a BNode
            return BNode(identifier=a_token)


    def _tune_prop(self, a_token):
        return Property(remove_corners(a_token))


    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_triples

    def _reset_count(self):
        self._error_triples = 0
        self._triples_count = 0

