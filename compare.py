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
