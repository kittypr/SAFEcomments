from lxml import etree
import odt_namespaces
import annotation
import difflib

# for key, value in odt_namespaces.namespaces.items():
#     etree.register_namespace(key, value)
#
# commented_tree = etree.parse("commented/content.xml")
# just_tree = etree.parse("not_commented/content.xml")
#
# commented_tree = etree.parse('commented/content.xml')
# for a in annotation.extract_annotations(commented_tree):
#     print(commented_tree.getpath(a.annotation_node), commented_tree.getpath(a.parent_node))

matcher = difflib.SequenceMatcher(None, string_1, string_2)
print(matcher.ratio())