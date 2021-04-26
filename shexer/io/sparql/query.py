from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.error import HTTPError
from time import sleep

from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

_FAKE_USER_AGENT = "Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)"
_RESULTS_KEY = "results"
_BINDINGS_KEY = "bindings"
_VALUE_KEY = "value"
_TYPE_KEY = "type"
_URI_TYPE = "uri"

_XML_LANG_FIELD = "xml:lang"


def _add_lang_if_needed(result_dict):
    result = result_dict[_VALUE_KEY]
    if _XML_LANG_FIELD in result_dict:
        result += '"' + result + '"@' + result_dict[_XML_LANG_FIELD]
    return result


def _add_corners_if_needed(target_elem, elem_type):
    if elem_type == _URI_TYPE and not target_elem.startswith("<"):
        return "<" + target_elem + ">"
    return target_elem


def query_endpoint_single_variable(endpoint_url, str_query, variable_id, max_retries=10, sleep_time=5, fake_user_agent=True):
    """
    It receives an SPARQL query with a single variable and returns a list with the resulting nodes

    :param endpoint_url:
    :param str_query:
    :param variable_id:
    :return:
    """
    first_failure = True
    sparql = SPARQLWrapper(endpoint_url)
    if fake_user_agent:
        sparql.agent = _FAKE_USER_AGENT
    sparql.setQuery(str_query)
    sparql.setReturnFormat(JSON)
    last_error = None
    while max_retries > 0:
        try:
            result_query = sparql.query().convert()
            result = []
            for row in result_query[_RESULTS_KEY][_BINDINGS_KEY]:
                # an_elem = _add_corners_if_needed(row[variable_id][_VALUE_KEY], row[variable_id][_TYPE_KEY])
                an_elem = row[variable_id][_VALUE_KEY]
                result.append(an_elem)
            return result
        except (HTTPError, EndPointInternalError) as e:
            max_retries -= 1
            sleep(sleep_time)
            last_error = e
            if first_failure and not fake_user_agent:
                sparql.agent = _FAKE_USER_AGENT
                first_failure = not first_failure
    last_error.msg = "Max number of attempts reached, it is not possible to perform the query. Msg:\n" + last_error.msg


def query_endpoint_po_of_an_s(endpoint_url, str_query, p_id, o_id, max_retries=5, sleep_time=2, fake_user_agent=True):
    first_failure = True
    sparql = SPARQLWrapper(endpoint_url)
    if fake_user_agent:
        sparql.agent = _FAKE_USER_AGENT
    sparql.setQuery(str_query)
    sparql.setReturnFormat(JSON)
    last_error = None
    while max_retries > 0:
        try:
            result_query = sparql.query().convert()
            result = []
            for row in result_query[_RESULTS_KEY][_BINDINGS_KEY]:
                # p_value = row[p_id][_VALUE_KEY]
                p_value = _add_corners_if_needed(target_elem=row[p_id][_VALUE_KEY],
                                                 elem_type=row[p_id][_TYPE_KEY])
                # o_value = _add_lang_if_needed(row[o_id])
                o_value = _add_corners_if_needed(target_elem=_add_lang_if_needed(row[o_id]),
                                                 elem_type=row[o_id][_TYPE_KEY])
                result.append((p_value, o_value))
            return result
        except (HTTPError, EndPointInternalError) as e:
            max_retries -= 1
            sleep(sleep_time)
            last_error = e
            if first_failure and not fake_user_agent:
                sparql.agent = _FAKE_USER_AGENT
                first_failure = not first_failure
    last_error.msg = "Max number of attempt reached, it is not possible to perform the query. Msg:\n" + last_error.msg