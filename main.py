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
    extractor = xml_extract.XMLExtractor(odt_filename, 'content.xml')
    extractor.extract()
    extractor.close()


def transfer_annotations(annotations_list):
    for a in annotations_list:
        new_parent_text = annotation.get_text(a.new_parent)
        c = compare.find_new_string(a.get_comment_text(), new_parent_text)
        print(c)
        if c is not None:
            print(new_parent_text[c[0]:c[0] + c[1]])
            print(c[-1])
        else:
            a.annotation_node.tail = a.new_parent.text
            a.new_parent.text = None
            a.new_parent.insert(0, a.annotation_node)


if __name__ == '__main__':
    register_namespaces()

    extract_xml(args.src)
    commented_tree = etree.parse('content.xml')
    annotations_list = annotation.extract_annotations(commented_tree)

    extract_xml(args.dest)
    not_commented_tree = etree.parse("content.xml")
    compare.compare(annotations_list, not_commented_tree)

    transfer_annotations(annotations_list)
    not_commented_tree.write(file=args.output, encoding='UTF-8', method='xml')
