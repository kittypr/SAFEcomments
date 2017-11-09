import odt_namespaces
import annotation
import difflib


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
    similarity = 0
    off = 0
    last_char = None
    sm = difflib.SequenceMatcher(None, string, text)
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
    while sm.ratio() > similarity:
        similarity = sm.ratio()
        last_char = text[-1]
        text = text[:-1]
        sm.set_seq2(text)
    if last_char is not None:
        text = text + last_char
    print(text)
    print('\n')
    return off, len(text), similarity

