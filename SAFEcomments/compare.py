import difflib

from SAFEcomments import annotation
from SAFEcomments import odt_namespaces


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
        p_text = annotation.get_text(p_node)
        if p_text == '':
            continue
        for annotation_node in annotations_list:
            ann_parent_text = annotation_node.get_text()
            similarity = difflib.SequenceMatcher(None, ann_parent_text, p_text).ratio()
            if similarity > ratios[i]:  # >= ??
                ratios[i] = similarity
                annotation_node.set_new_parent(p_node)
            i += 1
    for h_node in new_etree.findall('.//text:h', odt_namespaces.namespaces):
        i = 0
        p_text = annotation.get_text(h_node)
        if p_text == '':
            continue
        for annotation_node in annotations_list:
            ann_parent_text = annotation_node.get_text()
            similarity = difflib.SequenceMatcher(None, ann_parent_text, p_text).ratio()
            if similarity > ratios[i]:  # >= ??
                ratios[i] = similarity
                annotation_node.set_new_parent(h_node)
            i += 1
    for a in annotations_list:
        if a.new_parent is None and a.draw_frame is not None:
            path = '//draw:frame[@draw:name=\'' + a.draw_frame.attrib['{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name'] + '\']'
            node = new_etree.xpath(_path=path, namespaces=odt_namespaces.namespaces)[0]
            a.draw_frame = node
            if node is not None:
                a.new_parent = node.getparent()


def find_new_string(string, text, partly_deletion_similarity=0.6, exact_match_similarity=0.6):
    """Find new commented fragment in parent`s text.

    Used 3 different stages:

    1 - function tries to find exact match of given string.
    in success function ends work.
    2 - function tries to find the longest substring of given string.
    if length of substring good enough, function ends work.
    3 - function uses partly_deletion() algorythm of finding new segment.
    function ends work with result, if it is good enough.

    :param string: original commented segment.
    :param text: text of nes parent for annotation.
    :param exact_match_similarity: similarity of substring.
    :param partly_deletion_similarity: fuzzy similarity.

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
    if result[-1] / len(string) >= exact_match_similarity:
        return result[1], result[-1], result[-1] / len(string)
    result = partly_deletion(string, text)
    if result[-1] >= partly_deletion_similarity:
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
