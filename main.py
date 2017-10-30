import xml.etree.ElementTree as ET

ns = {"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
      "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
commentedTree = ET.parse("commented/content.xml")
justTree = ET.parse("not_commented/content.xml")

for annotationParent in commentedTree.findall(".//office:annotation/..", ns):
    annotation = annotationParent.find("./office:annotation", ns)
    annotationEnd = annotationParent.find("./office:annotation-end", ns)
    for p in justTree.findall(".//text:p", ns):
        if p.text.strip().find(annotation.tail.strip()) != -1:
            spl = p.text.split(annotation.tail.strip())
            p.text = spl[0]
            p.append(annotation)
            annotationEnd.tail = spl[1]
            p.append(annotationEnd)
justTree.write("not_commented/content_changed.xml", "UTF-8", True)

