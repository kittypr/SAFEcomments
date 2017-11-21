import odt_namespaces
import annotation
import difflib

EXACT_MATCH_SIMILARITY = 0.6
PARTLY_DELETION_SIMILARITY = 0.5


def compare(annotations_list, new_etree):
    ratios = [0] * len(annotations_list)
    for p_node in new_etree.findall('.//text:p', odt_namespaces.namespaces):
        i = 0
        for annotation_node in annotations_list:
            if difflib.SequenceMatcher(None, annotation_node.get_text(), annotation.get_text(p_node)).ratio() > ratios[i]:
                ratios[i] = difflib.SequenceMatcher(None, annotation_node.get_text(), annotation.get_text(p_node)).ratio()
                annotation_node.set_new_parent(p_node)
            i += 1


def find_new_string(string, text):
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
    similarity = 0
    off = 0
    last_char = None
    # print('String:', string)
    # print('Text:', text)
    sm = difflib.SequenceMatcher(None, string, text, False)
    while sm.ratio() > similarity:
        similarity = sm.ratio()
        last_char = text[0]
        text = text[1:]
        # print(len(text))
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
        # print(len(text))
        sm.set_seq2(text)
    if last_char is not None:
        text = text + last_char
    return off, len(text), similarity