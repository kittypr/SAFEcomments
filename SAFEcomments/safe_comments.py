#!/usr/bin/env python3
import argparse
import os

from lxml import etree

from SAFEcomments import annotation
from SAFEcomments import archive_handler
from SAFEcomments import compare
from SAFEcomments import odt_namespaces

exact_similarity = 0.6
fuzzy_similarity = 0.6


parser = argparse.ArgumentParser(description='This is simple utility program to transfer annotations from one odt file '
                                             'to another')
parser.add_argument('src', help='Input file with annotations to transfer. Use .odt extension.', action='store')
parser.add_argument('dest', help='Input file without annotations. Use .odt extension.', action='store')
parser.add_argument('output', help='Output file. Use .odt extension.', action='store')
parser.add_argument('-e', '-exact', help='Similarity of substring.', action='store')
parser.add_argument('-f', '-fuzzy', help='Fuzzy similarity.', action='store')
args = parser.parse_args()


def register_namespaces():
    for key, value in odt_namespaces.namespaces.items():
        etree.register_namespace(key, value)


def extract_xml(odt_filename):
    extr = archive_handler.ArchiveHandler(odt_filename)
    extr.extract('content.xml')
    return extr


def insert_on_text_in_child(node, parent_node, annotation_node, annotation_end_node, position, new_parent_text, current_len):
    children = node.getchildren()
    if node.text is not None:
        delta_len = len(node.text)
        if position[0] + position[1] in range(current_len + 1, current_len + delta_len + 1) and position[0] in range(current_len + 1, current_len + delta_len + 1):  # explain +1
            node.text = new_parent_text[current_len:position[0]]
            annotation_node.tail = new_parent_text[position[0]:position[0] + position[1]]
            annotation_end_node.tail = new_parent_text[position[0] + position[1]:current_len + delta_len]
            node.insert(0, annotation_node)
            node.insert(1, annotation_end_node)
            return -1
        elif position[0] in range(current_len + 1, current_len + delta_len + 1):
            node.text = new_parent_text[current_len:position[0]]
            annotation_node.tail = new_parent_text[position[0]:current_len + delta_len]
            node.insert(0, annotation_node)
        elif position[0] + position[1] in range(current_len + 1, current_len + delta_len + 1):
            node.text = new_parent_text[current_len:position[0] + position[1]]
            annotation_end_node.tail = new_parent_text[position[0] + position[1]:current_len + delta_len]
            node.insert(0, annotation_end_node)
            return -1
        current_len += delta_len
    if node.tag != '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation':
        for child in children:
            current_len = insert_on_text_in_child(child, node, annotation_node, annotation_end_node, position, new_parent_text, current_len)
            if current_len == -1:
                return -1
    if node.tail is not None:
        delta_len = len(node.tail)
        if position[0] in range(current_len + 1, current_len + delta_len + 1) and position[0] + position[1] in range(current_len + 1, current_len + delta_len + 1):
            node.tail = new_parent_text[current_len:position[0]]
            annotation_node.tail = new_parent_text[position[0]:position[0] + position[1]]
            annotation_end_node.tail = new_parent_text[position[0] + position[1]:current_len + delta_len]
            index = parent_node.index(node)
            parent_node.insert(index + 1, annotation_node)
            parent_node.insert(index + 2, annotation_end_node)
            return -1
        elif position[0] in range(current_len + 1, current_len + delta_len + 1):
            node.tail = new_parent_text[current_len:position[0]]
            annotation_node.tail = new_parent_text[position[0]:current_len + delta_len]
            index = parent_node.index(node)
            parent_node.insert(index + 1, annotation_node)
        elif position[0] + position[1] in range(current_len + 1, current_len + delta_len + 1):
            node.tail = new_parent_text[current_len:position[0] + position[1]]
            annotation_end_node.tail = new_parent_text[position[0] + position[1]:current_len + delta_len]
            index = parent_node.index(node)
            parent_node.insert(index + 1, annotation_end_node)
            return -1
        current_len += delta_len
    return current_len


def insert_annotation_on_text(ann, position, new_parent_text):  # position is tuple with (offset, len, similarity)
    try:
        current_len = len(ann.new_parent.text)
    except TypeError:
        current_len = 0
    children = ann.new_parent.getchildren()
    ann.annotation_node.tail = None
    ann.annotation_end_node.tail = None
    if current_len >= position[0]:
        if current_len >= position[0] + position[1]:
            ann.new_parent.text = new_parent_text[:position[0]]
            ann.annotation_node.tail = new_parent_text[position[0]:position[0] + position[1]]
            ann.annotation_end_node.tail = new_parent_text[position[0] + position[1]:current_len]
            ann.new_parent.insert(0, ann.annotation_node)
            ann.new_parent.insert(1, ann.annotation_end_node)
            return
        else:
            ann.new_parent.text = new_parent_text[:position[0]]
            ann.annotation_node.tail = new_parent_text[position[0]:current_len]
            ann.new_parent.insert(0, ann.annotation_node)
    for child in children:
        current_len = insert_on_text_in_child(child, ann.new_parent, ann.annotation_node, ann.annotation_end_node, position, new_parent_text, current_len)
        if current_len == -1:
            return


def insert_in_child(node, parent_node, annotation_node, position, new_parent_text, current_len):
    children = node.getchildren()
    if node.text is not None:
        delta_len = len(node.text)
        if position in range(current_len + 1, current_len + delta_len + 1):
            node.text = new_parent_text[current_len:position]
            annotation_node.tail = new_parent_text[position:current_len + delta_len]
            node.insert(0, annotation_node)
            return -1
        current_len += delta_len
    if node.tag != '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation':
        for child in children:
            current_len = insert_in_child(child, node, annotation_node, position, new_parent_text, current_len)
            if current_len == -1:
                return -1
    if node.tail is not None:
        delta_len = len(node.tail)
        if position in range(current_len + 1, current_len + delta_len + 1):
            node.tail = new_parent_text[current_len:position]
            annotation_node.tail = new_parent_text[position:current_len + delta_len]
            index = parent_node.index(node)
            parent_node.insert(index + 1, annotation_node)
            return -1
        current_len += delta_len
    return current_len


def insert_annotation(ann, position, new_parent_text):  # position is offset
    try:
        current_len = len(ann.new_parent.text)
    except TypeError:
        current_len = 0
    children = ann.new_parent.getchildren()
    ann.annotation_node.tail = None
    if current_len >= position:
        ann.new_parent.text = new_parent_text[:position]
        ann.annotation_node.tail = new_parent_text[position:current_len]
        ann.new_parent.insert(0, ann.annotation_node)
        return
    for child in children:
        current_len = insert_in_child(child, ann.new_parent, ann.annotation_node, position, new_parent_text, current_len)
        if current_len == -1:
            return


def insert_annotation_on_frame(ann, new_parent):
    new_parent.insert(new_parent.index(ann.draw_frame) - 1, ann.annotation_node)
    new_parent.insert(new_parent.index(ann.draw_frame) + 1, ann.annotation_end_node)


def insert_orphan(annotation_node, tree, annotation_end_node=None):
    text_node = tree.find('.//office:text', odt_namespaces.namespaces)
    p_node = etree.Element('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p')
    p_node.insert(0, annotation_node)
    if annotation_end_node is not None:
        p_node.insert(1, annotation_end_node)
    text_node.append(p_node)


def transfer_annotations(a_list, tree):
    for a in a_list:
        if a.new_parent is None:  # protects us against files without text
            insert_orphan(a.annotation_node, tree, a.annotation_end_node)
            continue
        new_parent_text = annotation.get_text(a.new_parent)
        if a.has_text:
            c = compare.find_new_string(a.get_annotation_text(), new_parent_text, fuzzy_similarity, exact_similarity)
            if c is not None:
                insert_annotation_on_text(a, c, new_parent_text)
            else:
                a.annotation_node.attrib.pop('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}name')
                insert_annotation(a, 0, new_parent_text)
        else:
            c1 = compare.find_new_string(a.get_annotation_tail(), new_parent_text, fuzzy_similarity, exact_similarity)
            c2 = compare.find_new_string(a.get_annotation_head(), new_parent_text, fuzzy_similarity, exact_similarity)
            if c1 is not None and c2 is not None:
                if c1[-1] > c2[-1]:
                    insert_annotation(a, c1[0], new_parent_text)
                else:
                    insert_annotation(a, c2[0] + c2[1], new_parent_text)
            elif c1 is not None:
                insert_annotation(a, c1[0], new_parent_text)
            elif c2 is not None:
                insert_annotation(a, c2[0] + c2[1], new_parent_text)
            elif a.draw_frame is not None:
                insert_annotation_on_frame(a, a.new_parent)
            else:
                insert_annotation(a, 0, new_parent_text)


if __name__ == '__main__':
    register_namespaces()

    if args.e:
        exact_similarity = float(args.e)
    if args.f:
        fuzzy_similarity = float(args.f)

    extractor = extract_xml(args.src)
    commented_tree = etree.parse('content.xml')
    annotations_list = annotation.extract_annotations(commented_tree)
    extractor.close()

    extractor = extract_xml(args.dest)
    not_commented_tree = etree.parse('content.xml')
    compare.compare(annotations_list, not_commented_tree)

    transfer_annotations(annotations_list, not_commented_tree)
    not_commented_tree.write('content.xml', encoding='UTF-8', method='xml')
    extractor.write('content.xml', args.output)
    os.remove('content.xml')
