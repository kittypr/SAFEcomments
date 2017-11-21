import odt_namespaces


class Annotation:

    def __init__(self, annotation_node, parent_node):
        self.annotation_node = annotation_node
        self.parent_node = parent_node
        self.new_parent = None

    def set_new_parent(self, new_parent):
        self.new_parent = new_parent

    def get_text(self):
        return get_text(self.parent_node)

    def get_comment_text(self):
        string = ''
        if self.annotation_node.tail:
            string += self.annotation_node.tail
        sibling = self.annotation_node.getnext()
        while sibling is not None and sibling.tag != '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation-end':
            string += get_text(sibling)
            sibling = sibling.getnext()
        return string


def extract_annotations(element_tree):
    annotations_list = []
    for annotation_node in element_tree.findall('.//office:annotation', odt_namespaces.namespaces):
        annotations_list.append(Annotation(annotation_node, annotation_node.getparent()))
    return annotations_list


def get_text(element):
    string = ''
    if element.text:
        string += element.text
    if element.tag != '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation':
        for e in element.iterchildren():
            string += get_text(e)
    if element.tail:
        string += element.tail
    return string
