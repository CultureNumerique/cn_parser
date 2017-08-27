#!/usr/bin/python
# coding: utf8


from io import open
import json

from lxml import etree
import shutil
import unittest
from collections import namedtuple
from six.moves import StringIO
import os
import logging
from pygiftparser import parser as pygift
from cnparser import model, toIMS, fromGift
from cnparser.settings import IMS_DIRECTORY, FOLDERS
# Ignore Warning
logger = logging.getLogger()
logger.setLevel(40)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


TEST_OUT_DIR = "./outTestIMS"
TEST_IMS_DIR = os.path.join(TEST_OUT_DIR, IMS_DIRECTORY)


def setUp():
    """
    Build IMS folder based on coursTest
    """
    with open("coursTest/module1/module_test.md",
              encoding='utf-8') as sample_file:
        global m
        m = model.Module(sample_file,
                         "tests",
                         "http://culturenumerique.univ-lille3.fr")
        m.toHTML()
        m_json = json.loads(m.toJson(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        if os.path.isdir(TEST_IMS_DIR):
            shutil.rmtree(TEST_IMS_DIR)
        m.ims_archive_path = toIMS.generateIMSArchive(m, TEST_OUT_DIR)
        sample_file.close()
        del m_json, sample_file


class IMSArchiveTestCase(unittest.TestCase):

    def testCreationDossierIMS(self):
        """
        Check if all directories and files are created
        """
        self.assertTrue(os.path.isdir(TEST_OUT_DIR),
                        "dir "+TEST_IMS_DIR+" don't exist")
        self.assertTrue(os.path.exists(os.path.join(TEST_OUT_DIR,
                                                    'tests.imscc.zip')),
                        "imscc.zip don't exist")
        for folder, message in zip(FOLDERS,
                                   ["dir Activite don't exist",
                                    "dir ActiviteAvancee don't exist",
                                    "dir Comprehension don't exist",
                                    "dir Comprehension don't exist",
                                    "dir webcontent don't exist"]):
            self.assertTrue(os.path.isdir(os.path.join(TEST_IMS_DIR,
                                                       folder)),
                            message)

        self.assertTrue(os.path.exists(os.path.join(TEST_IMS_DIR,
                                                    'imsmanifest.xml')),
                        "file imsmanifest.xml don't exist")
        print("[IMSArchiveTestCase]-- check_creation_dossier_ims OK --")

    def testNbWebContent(self):
        """
        """
        list_files_html = os.listdir(TEST_IMS_DIR+'/webcontent')
        self.assertEqual(len(list_files_html),
                         6,
                         "Not the same numbers of webcontent's files")
        print("[IMSArchiveTestCase]-- check_creation_webcontent OK --")

    def testNbWebActivite(self):
        """
        """
        list_files_ac = os.listdir(TEST_IMS_DIR+'/Activite')
        self.assertEqual(len(list_files_ac),
                         3,
                         "Not the same numbers of Activite's files")
        print("[IMSArchiveTestCase]-- check_creation_Activite OK --")

    def testNbWebComprehension(self):
        """
        """
        list_files_com = os.listdir(TEST_IMS_DIR+'/Comprehension')
        self.assertEqual(len(list_files_com),
                         4,
                         "Not the same numbers of Comprehension's files")
        print("[IMSArchiveTestCase]-- check_creation_Comprehension OK --")

    def testNbWebActiviteAvancee(self):
        """
        """
        list_files_acav = os.listdir(TEST_IMS_DIR+'/ActiviteAvancee')
        self.assertEqual(len(list_files_acav),
                         2,
                         "Not the same numbers of ActiviteAvancee's files")
        print("[IMSArchiveTestCase]-- check_creation_ActiviteAvancee OK --")

    def testGenerateIms(self):
        io_media = StringIO("""# Titre 1
## Titre 2
### Titre 3
Bienvenue sur le cours [!image](media/monimage3.png)
## Titre 2
blabla [!image](media/monimage2.png)
bloublou [!image](media/monimage3.png)
        """)
        m = model.Module(io_media, 'module1')
        for subsec in (m.sections[0].subsections):
            subsec.getFilename()

    def testArchitectureManifest(self):
        """
        """
        tree = etree.parse(TEST_IMS_DIR+'/imsmanifest.xml')
        root = tree.getroot()
        self.assertTrue('manifest' in root.tag,
                        'Not manifest root tag')
        for i, child in enumerate(root):
            if i == 0:
                self.assertTrue('metadata' in child.tag,
                                'Not metadata tag')
                self.assertTrue('schema' in child[0].tag,
                                'Not schema tag')
                self.assertTrue('IMS Common Cartridge' in child[0].text,
                                'Bad text for schema tag')
                self.assertTrue('schemaversion' in child[1].tag)
                self.assertTrue('1.1.0' in child[1].text)
                # lomimscc:lom
                self.assertTrue('lom' in child[2].tag)
                self.assertTrue('general' in child[2][0].tag)
                self.assertTrue('title' in child[2][0][0].tag)
                self.assertTrue('string' in child[2][0][0][0].tag)
                # self.assertTrue('fr' in
                # child[2][0][0][0].attrib.get('language'))

            # FIXME: à finir
        print("[IMSArchiveTestCase]-- check_architecture_imsmanifest OK --")


# Main
if __name__ == '__main__':
    setUp()
    unittest.main(verbosity=1)
