from lxml import etree
import odt_namespaces


class Annotation:

    def __init__(self, annotation_node, parent_node):
        self.annotation_node = annotation_node
        self.parent_node = parent_node

    #TODO par text


def extract_annotations(element_tree):
    annotations_list = []
    for annotation_node in element_tree.findall('.//office:annotation', odt_namespaces.namespaces):
        annotations_list.append(Annotation(annotation_node, annotation_node.getparent()))
    return annotations_list
