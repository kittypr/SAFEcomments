import zipfile
import os
import shutil
import sys


class ArchiveHandler(object):
    """Class that works with archive.

    It is a class, that creating with path to archive.
    After creating, it can:
    write file to archive -
    1)It makes dupe of archive, that it got during creation.
    2)During making dupe it writes new file to archive or rewrite file with same name.
    extract file from archive -
    1)Extract file with certain name from archive to script's directory.
    """

    def __init__(self, path):
        self.path = path
        self.archive = None

    def extract(self, name):
        """Extracting file from archive in script`s directory.

        :param name: the name of the file that need to be extracted.
        :return: False on errors, path to extracted file on success.
        """
        if not zipfile.is_zipfile(self.path):
            print('File you used is not archive. Extraction failed.')
            return False
        self.archive = zipfile.ZipFile(self.path, 'r')
        files = self.archive.infolist()
        exist = False
        member = None
        for f in files:
            if name == f.filename:
                member = f
                exist = True
        if not exist:
            print('There is no such file in archive ', self.path)
            self.archive.close()
            return False
        try:
            xml_extracted = self.archive.extract(member)
            return xml_extracted
        except PermissionError as err:
            print('There is no access to writing. Extraction failed')
            print(err.strerror)

    def close(self):
        """Method closes opened archive.
        """
        self.archive.close()

    def write(self, new_file, name):
        """Method makes dupe for archive from self.archive and replace file with new_file or add new_file.

        It forms new archive using relative path to script directory.
        So, to make archive from one file, it should be in script`s directory.
        
        :param new_file: path to new file.
        :param name: name for new archive.
        :return: False on errors, True on success
        """
        if not zipfile.is_zipfile(self.path):
            print('File you used is not archive. Writing failed.')
            return False
        self.archive = zipfile.ZipFile(self.path, 'r')
        files = self.archive.infolist()
        try:
            new_archive = zipfile.ZipFile(name, 'x')
        except PermissionError as err:
            print('There is no access to writing. Extraction failed')
            print(err.strerror)
            return False
        new_archive.write(new_file, os.path.relpath(new_file))
        redundant_dirs = set()
        for f in files:
            if os.path.basename(new_file) == f.filename:
                continue
            f_copy = self.extract(f.filename)
            new_archive.write(f_copy, os.path.relpath(f_copy))
            if os.path.relpath(f_copy) != os.path.basename(f_copy):
                if (os.path.dirname(f_copy)) not in redundant_dirs:
                    redundant_dirs.add(os.path.dirname(f_copy))
            else:
                os.remove(os.path.relpath(f_copy))
        cur_dir = os.path.normpath(sys.argv[0]).replace(os.path.basename(sys.argv[0]), '')
        print('CUR DIR: ', cur_dir)
        for red_dir in redundant_dirs:
            print('REDUCED DIRECTORY: ', red_dir)
            red_dir_ = red_dir.replace(cur_dir, '')
            print('DELETING DIRECTORY: ', red_dir_)
            if red_dir != red_dir_:
                try:
                    shutil.rmtree(red_dir_)
                except FileNotFoundError:
                    continue
        new_archive.close()
        return True


# module tests
if __name__ == '__main__':
    print(ArchiveHandler.__doc__)
