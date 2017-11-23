import zipfile
import os
import shutil
import sys


class XMLExtractor(object):

    def __init__(self, path):
        self.old_path = path
        self.old_archive = None

    def extract(self, need):
        if not zipfile.is_zipfile(self.old_path):
            print('You used a wrong file. Try again.')
            return False
        self.old_archive = zipfile.ZipFile(self.old_path, 'r')
        files = self.old_archive.infolist()
        exist = False
        member = None
        for f in files:
            if need == f.filename:
                member = f
                exist = True
        if not exist:
            print('There is no such file in archive ', self.old_path)
            self.old_archive.close()
            return False
        xml_extracted = self.old_archive.extract(member)
        return xml_extracted

    def close(self):
        self.old_archive.close()

    def write(self, new_xml, name):
        if not zipfile.is_zipfile(self.old_path):
            print('You used a wrong file. Try again.')
            return False
        self.old_archive = zipfile.ZipFile(self.old_path, 'r')
        files = self.old_archive.infolist()
        new_archive = zipfile.ZipFile(name, 'x')
        new_archive.write(new_xml, os.path.relpath(new_xml))
        os.remove(os.path.relpath(new_xml))
        redundant_dirs = set()
        for f in files:
            if os.path.basename(new_xml) == f.filename:
                continue
            f_copy = self.extract(f.filename)
            new_archive.write(f_copy, os.path.relpath(f_copy))
            if os.path.relpath(f_copy) != os.path.basename(f_copy):
                if (os.path.dirname(f_copy)) not in redundant_dirs:
                    redundant_dirs.add(os.path.dirname(f_copy))
            else:
                os.remove(os.path.relpath(f_copy))
        cur_dir = os.path.normpath(sys.argv[0]).replace('xml_extract.py', '')
        for red_dir in redundant_dirs:
            red_dir_ = red_dir.replace(cur_dir, '')
            if red_dir != red_dir_:
                try:
                    shutil.rmtree(red_dir_)
                except FileNotFoundError:
                    continue
        new_archive.close()


if __name__ == '__main__':
    s = 'a'.replace('a', '')
    print(s)
    xml_extractor = XMLExtractor('test_data/full_p_com.odt')
    path_ = xml_extractor.extract('content.xml')
    print(path_)

    xml_extractor.close()
    xml_extractor = XMLExtractor('test_data/full_p.odt')
    xml_extractor.write(path_, 'new_odt.odt')


