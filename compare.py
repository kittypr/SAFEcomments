import odt_namespaces
import annotation
import difflib

MIN_SIMILARITY = 0.8

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
    global MIN_SIMILARITY
    result = partly_deletion(string, text)
    if result[-1] >= MIN_SIMILARITY:
        return result
    sm = difflib.SequenceMatcher(None, string, text, False)
    result = sm.find_longest_match(0, len(string), 0, len(text))
    if result[-1]/len(string) >= MIN_SIMILARITY:
        return result[1], result[-1], result[-1]/len(string)
    return None


def partly_deletion(string, text):
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