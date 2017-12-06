import odt_namespaces


class Annotation:

    def __init__(self, annotation_node, parent_node):
        self.annotation_node = annotation_node
        self.annotation_end_node = None
        self.parent_node = parent_node
        self.new_parent = None
        self.has_text = False
        self.annotation_text = None
        self.parent_text = None
        self.annotation_tail = None
        self.annotation_head = None

    def set_new_parent(self, new_parent):
        self.new_parent = new_parent

    def get_text(self):
        if self.parent_text is None:
            self.parent_text = get_text(self.parent_node)
        return self.parent_text

    def extract_annotation_text(self):
        string = ''
        if self.annotation_node.tail:
            string += self.annotation_node.tail
        parent = self.annotation_node
        while parent != self.parent_node:
            sibling = parent.getnext()
            while sibling is not None and (self.annotation_end_node is not None and sibling != self.annotation_end_node):
                string += get_text(sibling)
                sibling = sibling.getnext()
            parent = parent.getparent()
        if string == '':
            self.annotation_text = None
            self.has_text = False
        else:
            self.annotation_text = string
            self.has_text = True

    def get_annotation_text(self):  # TODO exception when None
        # if self.annotation_text is None:
        #     raise ValueError('annotation text is None.')
        return self.annotation_text

    def extract_annotation_tail(self):
        if not self.has_text:
            string = ''
            if self.annotation_node.tail:
                string += self.annotation_node.tail
            sibling = self.annotation_node.getnext()
            while sibling is not None:
                string += get_text(sibling)
                sibling = sibling.getnext()
            if string == '':
                self.annotation_tail = None
            else:
                self.annotation_tail = string

    def get_annotation_tail(self):
        # if self.annotation_tail is None:
        #     raise ValueError('annotation tail is None.')
        return self.annotation_tail

    def extract_annotation_head(self):
        string = ''
        if self.parent_node.text:
            string += self.parent_node.text
        children = self.parent_node.getchildren()
        for child in children:
            if child == self.annotation_node:
                break
            string += get_text(child)
        if string == '':
            self.annotation_head = None
        else:
            self.annotation_head = string

    def get_annotation_head(self):
        # if self.annotation_head is None:
        #     raise ValueError('annotation head is None.')
        return self.annotation_head


def find_matching_parent(annotation):
    parent = annotation.getparent()
    while parent.tag is not None and parent.tag != '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p':
        print(parent.tag)
        parent = parent.getparent()
    return parent


def extract_annotations(element_tree):
    annotations_list = []
    for annotation_node in element_tree.findall('.//office:annotation', odt_namespaces.namespaces):
        a = Annotation(annotation_node, find_matching_parent(annotation_node))
        annotations_list.append(a)
        if '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}name' in a.annotation_node.keys():
            path = '//office:annotation-end[@office:name=\'' + a.annotation_node.attrib['{urn:oasis:names:tc:opendocument:xmlns:office:1.0}name'] + '\']'
            a.annotation_end_node = element_tree.xpath(_path=path, namespaces=odt_namespaces.namespaces)[0]
            a.extract_annotation_text()
        else:
            a.extract_annotation_tail()
            a.extract_annotation_head()
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
