import difflib

import annotation
import odt_namespaces


EXACT_MATCH_SIMILARITY = 0.6  # similarity of substring
PARTLY_DELETION_SIMILARITY = 0.5  # fuzzy similarity


def compare(annotations_list, new_etree):
    """ This function fine new parent for every annotation.

    For every object that represent annotations we find and writewrite new parent as it's attribute
    using fuzzy string comparison.

    :param annotations_list: list of annotations.
    :param new_etree: element tree of file with newer version.
    :return: nothing.
    """
    ratios = [0] * len(annotations_list)
    for p_node in new_etree.findall('.//text:p', odt_namespaces.namespaces):
        i = 0
        for annotation_node in annotations_list:
            similarity = difflib.SequenceMatcher(None, annotation_node.get_text(), annotation.get_text(p_node)).ratio()
            if similarity > ratios[i]:  # >= ??
                ratios[i] = similarity
                annotation_node.set_new_parent(p_node)
            i += 1


def find_new_string(string, text):
    """Find new commented fragment in parent`s text.

    Used 3 different stages:

    1 - function tries to find exact match of given string.
    in success function ends work.
    2 - function tries to find the longest substring of given string.
    if length of substring good enough, function ends work.
    3 - function uses partly_deletion() algorythm of finding new segment.
    function ends work with result, if it is good enough.

    :param string: original commented segment
    :param text: text of nes parent for annotation

    :return: set, that consists of 0 - start position in new text, 1 - length, 2 - similarity on success,
             None in other case.
    """
    if string is None or text is None:
        return None
    find_result = text.find(string)
    if find_result != -1:
        return find_result, len(string), 1
    sm = difflib.SequenceMatcher(None, string, text, False)
    result = sm.find_longest_match(0, len(string), 0, len(text))
    global EXACT_MATCH_SIMILARITY
    if result[-1] / len(string) >= EXACT_MATCH_SIMILARITY:
        return result[1], result[-1], result[-1] / len(string)
    result = partly_deletion(string, text)
    global PARTLY_DELETION_SIMILARITY
    if result[-1] >= PARTLY_DELETION_SIMILARITY:
        return result
    return None


def partly_deletion(string, text):
    """This function is our realisation of fuzzy substring search.

    It deletes symbol from beginning and makes fuzzy comparison.
    If result began better, it repeats this action until result lessen.
    After tha, it return las deleted symbol on it`s place and do the same process but
    starts from ending.

    :param string: original commented segment
    :param text: text of nes parent for annotation

    :return: set, that consists of 0 - start position in new text, 1 - length, 2 - similarity
    """
    similarity = 0
    off = 0
    last_char = None
    sm = difflib.SequenceMatcher(None, string, text, False)
    while sm.ratio() > similarity:
        similarity = sm.ratio()
        last_char = text[0]
        text = text[1:]
        off += 1
        sm.set_seq2(text)
    if last_char is not None:
        text = last_char + text
        off -= 1
    last_char = None
    similarity = 0
    while sm.ratio() > similarity:
        similarity = sm.ratio()
        last_char = text[-1]
        text = text[:-1]
        sm.set_seq2(text)
    if last_char is not None:
        text = text + last_char
    return off, len(text), similarity
