from lxml import etree
import odt_namespaces
import annotation
import compare
import xml_extract

for key, value in odt_namespaces.namespaces.items():
    etree.register_namespace(key, value)

extractor = xml_extract.XMLExtractor('commented/test.odt', 'content.xml')
extractor.extract()
extractor.close()

commented_tree = etree.parse('content.xml')
annotations_list = annotation.extract_annotations(commented_tree)

extractor = xml_extract.XMLExtractor('not_commented/test.odt', 'content.xml')
extractor.extract()
extractor.close()

new_etree = etree.parse("content.xml")
compare.compare(annotations_list, new_etree)
for a in annotations_list:
    print(new_etree.getpath(a.new_parent))