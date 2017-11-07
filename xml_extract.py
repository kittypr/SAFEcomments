import zipfile


class XMLExtractor(object):

    def __init__(self, path, need, ):
        self.old_path = path
        self.need = need
        self.old_archive = None

    def extract(self):
        if not zipfile.is_zipfile(self.old_path):
            print('You used a wrong file. Try again.')
            return False
        self.old_archive = zipfile.ZipFile(self.old_path, 'r')
        files = self.old_archive.infolist()
        exist = False
        member = None
        for f in files:
            if self.need == f.filename:
                member = f
                exist = True
        if not exist:
            print('There is no such file in archive ', self.old_path)
            self.old_archive.close()
            return False
        xml_extracted = self.old_archive.extract(member)
        self.old_archive.close()
        return xml_extracted

    def close(self):
        self.old_archive.close()


if __name__ == '__main__':
    xml_extractor = XMLExtractor('test.odt', 'content.xml', 'copytest.odt')
    path_ = xml_extractor.extract()
    print(path_)
    xml_extractor.close()

