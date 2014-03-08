# -*- coding: utf -*-
import pdb

import os
import os.path
import re
import urllib
import codecs

import markdown2
from jinja2 import Environment, FileSystemLoader

from Tools import *
from config import *


class Post(object):
    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        self._parse_md(filepath)

    @property
    def mtime(self):
        return Utils.to_time(Utils.parse_time(os.stat(self.filepath).st_mtime))

    @property
    def filename(self):
        return os.path.basename(self.filepath).split('.')[0]

    @property
    def url(self):
        return urllib.quote(Utils.to_utf8(self.htmlfile))

    @property
    def title(self):
        for line in self.metalines:
            if line.startswith('Title:'):
                return line.split(':', 1)[1].strip()
        return self.filename

    @property
    def date(self):
        for line in self.metalines:
            if line.startswith('Date:'):
                return Utils.parse_time(line.split(':', 1)[1].strip())
        return Utils.parse_time(self.mtime)

    @property
    def htmlfile(self):
        return '-'.join([Utils.to_time(self.date), self.title]) + '.html'

    @property
    def description(self):
        for line in self.metalines:
            if line.startswith('Description:'):
                return line.split(':', 1)[1].strip()

    @property
    def content(self):
        return Utils.to_unicode(markdown2.markdown(self.bodycontent,
                                extras=['code-friendly',
                                        'fenced-code-blocks']))

    def _parse_md(self, filepath):
        if os.path.isdir(filepath):
            mdfiles = [x for x in os.listdir(filepath)\
                        if x.split('.')[-1] in Markdown_extensions]
            md_path = os.path.join(filepath, mdfiles[0])
        elif (os.path.isfile(filepath) and
                filepath.split('.')[-1] in Markdown_extensions):
            md_path = filepath
        else:
            print('Not a valid filepath, need markdown file\
                    or A directory contains markdown file)')
            sys.exit()

        try:
            f = open(md_path)
        except:
            print('Open markdown file failed.')
        else:
            header = ''
            body = ''
            header_flag = True
            for line in f:
                if header_flag and\
                    (line.startswith('---') or line.startswith('===')):
                    header_flag = False
                elif header_flag:
                    header += line
                else:
                    body += line
            f.close()

        self.metalines = [Utils.to_unicode(line)\
                        for line in header.split('\n') if line]
        self.bodycontent = Utils.to_unicode(body)

        if os.path.isdir(self.filepath):
            newcontent = []
            for line in self.bodycontent.split('\n'):
                newcontent.append(Utils.images_process(Utils.to_time(self.date), line))
            self.bodycontent = '\n'.join(newcontent)

    def _process_imgs(self):
        img_path = os.path.join(Deployed_folder, 'img', Utils.to_time(self.date))
        if not os.path.exists(img_path):
            try:
                os.makedirs(img_path, 0755)
            except IOError as e:
                print('Create related img path failed. Error: %s' % e)

        for img in [img for img in os.listdir(self.filepath)\
                    if img.split('.')[-1] in Image_extensions]:
            shutil.copyfile(os.path.abspath(os.path.join(self.filepath, img)),
                            os.path.abspath(os.path.join(img_path, img)))

    def to_html(self):
        if os.path.isdir(self.filepath):
            self._process_imgs()

        env = Environment(loader=FileSystemLoader(Template_path))
        env.filters['showtime'] = Utils.to_time
        template = env.get_template('article.html')
        try:
            f = codecs.open(
                    os.path.join(Deployed_folder, self.htmlfile),
                    'w',
                    'utf-8')
            f.write(template.render(article=self,
                                    page_title=self.title,
                                    description=self.description))
            f.close()
        except IOError as e:
            print('Build article failed. Error: %s' % e)


class Pagination(object):
    def __init__(self, page_number, pages, per_page):
        self.page_number = page_number + 1
        self.pages = pages
        self.per_page = per_page

    @property
    def start_point(self):
        return (self.page_number - 1) * self.per_page
    
    @property
    def end_point(self):
        return (self.page_number - 1) * self.per_page + self.per_page

    @property
    def has_prev(self):
        return self.page_number > 1

    @property
    def prev_number(self):
        return self.page_number - 1

    @property
    def has_next(self):
        return self.page_number < self.pages

    @property
    def next_number(self):
        return self.page_number + 1


class Page(object):
    def __init__(self, postlist):
        self.postlist = postlist

    def _sort_postlist(self, reverse=True):
        self.sorted_postlist = []

        tmp_list = []
        for post in self.postlist:
            tmp_list.append(tuple([Utils.parse_time(post.date), post]))

        if reverse:
            tmp_list.sort(reverse=True)
        else:
            tmp_list.sort()

        for t in tmp_list:
            self.sorted_postlist.append(t[1])

        return self.sorted_postlist

    def to_pagehtml(self):
        self._sort_postlist()

        total = len(self.sorted_postlist)
        per_page = Page_quantity

        if total % per_page == 0:
            pages = total / per_page
        else:
            pages = total /per_page + 1

        pages_flag = False
        if pages > 1:
            pages_flag = True

        for p in xrange(pages):
            pagination = Pagination(p, pages, per_page)

            env = Environment(loader=FileSystemLoader(Template_path))
            template = env.get_template('page.html')
            try:
                if not os.path.exists(os.path.join(Deployed_folder, 'page')):
                    os.mkdir(os.path.join(Deployed_folder, 'page'), 0755)

                f = codecs.open(
                        os.path.join(Deployed_folder,
                                    'page',
                                    str(pagination.page_number)+'.html'),
                        'w',
                        'utf-8')
                f.write(template.render(
                        articles=self.sorted_postlist\
                                [pagination.start_point:pagination.end_point],
                        page_title=Blog_name+' Page '+str(pagination.page_number),
                        pages_flag=pages_flag,
                        pagination=pagination))
                f.close()
            except IOError as e:
                print('Build page failed. Error: %s' % e)

    def to_indexhtml(self):
        self._sort_postlist()

        pages = False
        if len(self.sorted_postlist) > Index_quantity:
            pages = True

        env = Environment(loader=FileSystemLoader(Template_path))
        template = env.get_template('index.html')
        try:
            f = codecs.open(
                    os.path.join(Deployed_folder, 'index.html'),
                    'w',
                    'utf-8')
            f.write(template.render(
                        articles=self.sorted_postlist[:Index_quantity],
                        page_title=Blog_name,
                        pages=pages))
            f.close()
        except IOError as e:
            print('Build index failed. Error: %s' % e)

    def to_feedxml(self):
        self._sort_postlist()

        env = Environment(loader=FileSystemLoader(Template_path))
        template = env.get_template('feed.xml')
        try:
            f = codecs.open(
                    os.path.join(Deployed_folder, 'feed.xml'),
                    'w',
                    'utf-8')
            f.write(template.render(
                        blog_name=Blog_name,
                        updated_time=Utils.to_time(datetime.datetime.now()),
                        articles=self.sorted_postlist[:Feed_quantity]))
            f.close()
        except IOError as e:
            print('Build feed failed. Error: %s' % e)
        

if __name__ == '__main__':
    #post = Post(r'/tmp/Sources/1.md')
    post = Post(r'/tmp/Sources/pkg')
    post.to_html()
    #post._get_imgs()
    #post1 = Post(u'/tmp/Sources/中文.md')
    #post2 = Post(u'/tmp/Sources/1.md')
    #post3 = Post(u'/tmp/Sources/2.md')
    #post4 = Post(u'/tmp/Sources/3.md')

    #page = Page([post1, post2, post3, post4])
    #post1.to_html()
    #post2.to_html()
    #post3.to_html()
    #post4.to_html()
    #page.to_indexhtml()
    #page.to_pagehtml()
    #post.to_html()
    #writer = Writer()
    #writer.generate_article(u'/tmp/Sources/中文2.md')
    #writer.generate_index(writer._sort_articles());
    #writer.generate_page(writer._sort_articles());
    #writer.generate_article('/tmp/Sources/2.md')
    #writer.generate_article('/tmp/Sources/3.md')
    #writer.generate_article('/tmp/Sources/4.md')
    #writer._sort_articles()
