# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import shutil
import markdown
import os
import logging

from cnparser import utils
from cnparser.settings import HTML_THEMES_PATH, \
    DEFAULT_THEME_PATH, MARKDOWN_EXT, LOGO_EXTENSIONS


def getMeta(repoDir, theme_path=None, single=False):
    # prepare HTML templates
    user_meta_path = os.path.join(repoDir, 'templates')

    if theme_path is None:
        list_base_path = [user_meta_path,
                          DEFAULT_THEME_PATH]
    else:
        list_base_path = [user_meta_path,
                          theme_path,
                          DEFAULT_THEME_PATH]

    jenv = Environment(loader=FileSystemLoader(list_base_path))
    jenv.filters['slugify'] = utils.cnslugify
    meta = {}
    meta['site'] = jenv.get_template("site_layout.tmpl")
    meta['module'] = jenv.get_template("module.tmpl")
    meta['index'] = jenv.get_template("index.tmpl")

    # if found, copy logo.png, else use default
    logo_files = [os.path.join(b, "logo."+e)
                  for b in list_base_path for e in LOGO_EXTENSIONS]
    for lpath in logo_files:
        if os.path.exists(lpath):
            meta['logo'] = lpath
            break

    # open and parse 1st line title.md
    meta['title'] = "Titre de ce cours"
    if os.path.exists(os.path.join(user_meta_path, 'title.md')):
        try:
            title_file = os.path.join(user_meta_path, 'title.md')
            with open(title_file, 'r', encoding='utf-8') as f:
                meta['title'] = f.read().strip()
        except Exception as e:
            logging.warning(" Error while parsing title file %s" % e)

    if single:
        return meta

    meta['home'] = ''
    user_home_html = os.path.join(user_meta_path, 'home.html')
    user_home_md = os.path.join(user_meta_path, 'home.md')
    theme_home_html = os.path.join(theme_path, 'home.html')
    default_home_html = os.path.join(DEFAULT_THEME_PATH, 'home.html')
    if os.path.exists(user_home_html):
        try:
            with open(user_home_html, 'r', encoding='utf-8') as f:
                meta['home'] = f.read()
        except Exception:
            logging.error('Cannot read %s' % user_home_html)
    elif os.path.exists(user_home_md):
        try:
            with open(user_home_md, 'r', encoding='utf-8') as f:
                meta['home'] = markdown.markdown(f.read(), MARKDOWN_EXT)
        except Exception:
            logging.error('Cannot read or parse %s' % user_home_md)
    elif os.path.exists(theme_home_html):
        try:
            with open(theme_home_html, 'r', encoding='utf-8') as f:
                meta['home'] = f.read()
        except Exception:
            logging.error('Cannot read %s' % theme_home_html)
    else:
        try:
            with open(default_home_html, 'r', encoding='utf-8') as f:
                meta['home'] = f.read()
        except Exception:
            logging.error('Cannot read %s' % default_home_html)
    return meta


def buildSiteMultiple(course_program, repoDir, outDir, theme_path=None):
    # Create site index.html with home.md content
    # open and parse home.md
    meta = getMeta(repoDir, theme_path)
    course_program.title = meta['title']
    index_content = meta['index'].render(course=course_program,
                                         home_content=meta['home'])
    # write index.html file
    index_html = meta['site'].render(course=course_program,
                                     content=index_content,
                                     body_class="home",
                                     logo=meta['logo'])
    utils.write_file(index_html, os.getcwd(), outDir, 'index.html')

    # Loop through modules
    for module in course_program.modules:
        module_html_content = meta['module'].render(module=module)
        html = meta['site'].render(course=course_program,
                                   content=module_html_content,
                                   body_class="modules",
                                   logo=meta['logo'])
        utils.write_file(html, os.getcwd(), outDir, module.name+'.html')

    shutil.copy(meta['logo'], outDir)


def buildSiteSingle(course_program, repoDir, outDir, theme_path):
    meta = getMeta(repoDir, theme_path, single=True)
    course_program.title = meta['title']

    # Loop through modules
    if len(course_program.modules) == 1:
        module = course_program.modules[0]
        module_html_content = meta['module'].render(module=module)
        html = meta['site'].render(course=course_program,
                                   content=module_html_content,
                                   body_class="single",
                                   logo=meta['logo'])
        utils.write_file(html, os.getcwd(), outDir, module.name+'.html')

    shutil.copy(meta['logo'], outDir)


def buildSite(course_program, repoDir, outDir, theme):
    """ Generate full site from result of parsing repository """

    theme_path = os.path.join(HTML_THEMES_PATH, theme)
    if len(course_program.modules) > 1:
        buildSiteMultiple(course_program, repoDir, outDir, theme_path)
    else:
        buildSiteSingle(course_program, repoDir, outDir, theme_path)
