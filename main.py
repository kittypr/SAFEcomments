import xml.etree.ElementTree as ElementTree

# ns = {"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
#      "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
commented_tree = ElementTree.parse("commented/content.xml")
just_tree = ElementTree.parse("not_commented/content.xml")

for annotation_parent in commented_tree.findall('.//{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation/..'):
    annotation = annotation_parent.find('./{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation')
    annotation_end = annotation_parent.find('./{urn:oasis:names:tc:opendocument:xmlns:office:1.0}annotation-end')
    for p in just_tree.findall('.//{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
        if p.text.strip().find(annotation.tail.strip()) != -1:
            spl = p.text.split(annotation.tail.strip())
            p.text = spl[0]
            p.append(annotation)
            annotation_end.tail = spl[1]
            p.append(annotation_end)
just_tree.write('not_commented/content_changed.xml', 'UTF-8', True)
