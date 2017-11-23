import odt_namespaces


class Annotation:

    def __init__(self, annotation_node, parent_node):
        self.annotation_node = annotation_node
        self.parent_node = parent_node
        self.new_parent = None
        self.has_text = False
        self.annotation_text = None

    def set_new_parent(self, new_parent):
        self.new_parent = new_parent

    def get_text(self):
        return get_text(self.parent_node)

    def get_annotation_text(self):
        if not self.has_text:
            return None
        string = ''
        if self.annotation_node.tail:
            string += self.annotation_node.tail
        sibling = self.annotation_node.getnext()
        while True:
            while sibling is not None and sibling.tag != '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation-end':
                string += get_text(sibling)
                sibling = sibling.getnext()
            if sibling is None:
                sibling = self.parent_node.getnext()
            else:
                return string

    def get_annotation_tail(self):
        if self.has_text:
            return None
        string = ''
        if self.annotation_node.tail:
            string += self.annotation_node.tail
        sibling = self.annotation_node.getnext()
        while sibling is not None:
            string += get_text(sibling)
            sibling = sibling.getnext()
        return string

    def get_annotation_head(self):
        string = ''
        if self.parent_node.text:
            string += self.parent_node.text
        children = self.parent_node.getchildren()
        for child in children:
            if child.tag == '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation':
                break
            string += get_text(child)
        return string


def extract_annotations(element_tree):
    annotations_list = []
    for annotation_node in element_tree.findall('.//office:annotation', odt_namespaces.namespaces):
        a = Annotation(annotation_node, annotation_node.getparent())
        annotations_list.append(a)
        if '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}name' in a.annotation_node.keys():
            a.has_text = True
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
