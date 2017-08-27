# -*- coding: utf-8 -*-
import os


MARKDOWN_EXT = ['markdown.extensions.extra', 'superscript']
# BASE_PATH for source and dest and for templates
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(BASE_PATH, 'logs', 'cnparser.log')


# IMS directory name (usually located in each modules directory)
IMS_DIRECTORY = 'IMS'

# folders associated with activity types
FOLDERS = ['Activite', 'ActiviteAvancee', 'Comprehension', 'webcontent']

LOGO_EXTENSIONS = ['png', 'jpg', 'gif']
HTML_THEMES_PATH = os.path.join(BASE_PATH, 'templates', 'toHTML')
DEFAULT_THEME_PATH = os.path.join(HTML_THEMES_PATH, 'default')
DEFAULT_LOGO_MODULE = os.path.join('static', 'img', 'module.svg')
VIDEO_THUMB_API_URL = 'https://vimeo.com/api/v2/video/'
DEFAULT_VIDEO_THUMB_URL = 'https://i.vimeocdn.com/video/536038298_640.jpg'
DEFAULT_BASE_URL = 'http://culturenumerique.univ-lille3.fr'

# EDX directory name (usually located in each modules directory)
EDX_DIRECTORY = 'EDX'
EDX_TEMPLATES_PATH = os.path.join(BASE_PATH,
                                  'templates',
                                  'toEDX')
EDX_DEFAULT_FILES = {
    'about': 'overview.html',
    'assets': 'assets.xml',
    'info': 'updates.html',
    'policies': 'assets.json'
}
EDX_ADVANCED_MODULE_LIST = ['cnvideo', 'library_content']
EDX_GRADER_MAP = {
    'Activite': 'Activite',
    'ActiviteAvancee': 'Activite Avancee',
    'Comprehension': 'Comprehension',
    'webcontent': None
}
