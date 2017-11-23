from lxml import etree
import odt_namespaces
import annotation
import compare
import xml_extract
import argparse

parser = argparse.ArgumentParser(description='This is simple utility program to transfer annotations from one odt file '
                                             'to another')
parser.add_argument('src', help='Input file with annotations to transfer. Use .odt extension.', action='store')
parser.add_argument('dest', help='Input file without annotations. Use .odt extension.', action='store')
parser.add_argument('output', help='Output file. Use .odt extension.', action='store')
args = parser.parse_args()


def register_namespaces():
    for key, value in odt_namespaces.namespaces.items():
        etree.register_namespace(key, value)


def extract_xml(odt_filename):
    extractor = xml_extract.XMLExtractor(odt_filename)
    extractor.extract('content.xml')
    return extractor


def transfer_annotations(annotations_list):
    for a in annotations_list:
        new_parent_text = annotation.get_text(a.new_parent)
        if a.has_text:
            c = compare.find_new_string(a.get_annotation_text(), new_parent_text)
            if c is not None:
                print(new_parent_text[c[0]:c[0] + c[1]])
                print(c[-1])
            else:
                a.annotation_node.tail = a.new_parent.text
                a.new_parent.text = None
                a.new_parent.insert(0, a.annotation_node)  # TODO remove office:name attribute
        else:
            c1 = compare.find_new_string(a.get_annotation_tail(), new_parent_text)
            c2 = compare.find_new_string(a.get_annotation_head(), new_parent_text)
            if c1 is not None and c2 is not None:
                c = c1 if c1[-1] > c2[-1] else c2
                place = 'tail'
            elif c1 is not None:
                c = c1
                place = 'tail'
            else:
                c = c2
                place = 'head'
            if c is not None:
                if place == 'tail':
                    a.annotation_node.tail = a.new_parent.text[c[0]:len(a.new_parent.text)]
                    a.new_parent.text = a.new_parent.text[0:c[0]]
                    a.new_parent.insert(0, a.annotation_node)
                else:
                    a.annotation_node.tail = a.new_parent.text[c[0] + c[1]:len(a.new_parent.text)]
                    a.new_parent.text = a.new_parent.text[0:c[0] + c[1]]
                    a.new_parent.insert(0, a.annotation_node)
            else:
                a.annotation_node.tail = a.new_parent.text
                a.new_parent.text = None
                a.new_parent.insert(0, a.annotation_node)  # TODO remove office:name attribute


if __name__ == '__main__':
    register_namespaces()

    extractor = extract_xml(args.src)
    commented_tree = etree.parse('content.xml')
    annotations_list = annotation.extract_annotations(commented_tree)
    extractor.close()

    extractor = extract_xml(args.dest)
    not_commented_tree = etree.parse("content.xml")
    compare.compare(annotations_list, not_commented_tree)

    transfer_annotations(annotations_list)
    not_commented_tree.write('content.xml', encoding='UTF-8', method='xml')
    extractor.write('content.xml', args.output)
