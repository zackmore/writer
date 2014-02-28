# -*- coding: utf-8 -*-

import pdb
import os.path
import time
import pygments
import markdown2

from model import Category, Article, Tag
from config import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Utils(object):
    def __init__(self):
        engine = create_engine('sqlite:///'+db_path)
        Session = scoped_session(sessionmaker(bind=engine))
        self.db = Session()

    def _to_unicode(self, value):
        if isinstance(value, unicode):
            return value
        if isinstance(value, basestring):
            return value.decode('utf-8')
        if isinstance(value, int):
            return str(value)
        if isinstance(value, bytes):
            return value.decode('utf-8')
        return value

    def _utf8(value):
        if isinstace(value, (bytes, type(None), str)):
            return value
        if isinstance(value, int):
            return str(value)
        assert isinstance(value, unicode)
        return value.encode('utf-8')

    def _parse_meta(self, header):
        meta = {}

        meta_groups = header.split('\n')
        for group in meta_groups:
            if group.startswith('#'):
                meta['title'] = group.split('#')[1].strip()
            elif group.startswith('-'):
                if group.find('date') > 0:
                    meta['date'] = group.split(':')[1].strip()
                if group.find('category') > 0:
                    meta['category'] = group.split(':')[1].strip()
                if group.find('tags') > 0:
                    meta['tags'] = [x.strip() for x in
                                    group.split(':')[1].strip().split(',')]

        return meta

    def parse_md(self, filepath):
        '''
        returned

        {
            'meta': {
                'title': 'title string',
                'category': 'category string',
                'tags': [tag1, tag2, tag3],
                'date': 'date string',
                'mdfile': 'path/to/file',
            },
            'body': 'HTML block (markdowned)'
        }
        '''

        md_handle = open(filepath)

        header = ''
        body = ''
        header_flag = True
        for line in md_handle:
            if header_flag and\
                (line.startswith('---') or line.startswith('===')):
                header_flag = False
            elif header_flag:
                header += line
            else:
                body += line

        md_handle.close()

        md_meta = self._parse_meta(self._to_unicode(header))
        md_body = markdown2.markdown(self._to_unicode(body),
                                    extras=['code-friendly',
                                            'fenced-code-blocks'])

        if 'title' not in md_meta:
            md_meta['title'] = os.path.basename(filepath).split('.')[0]
        if 'category' not in md_meta:
            md_meta['category'] = 'Uncategoried'
        if 'date' not in md_meta:
            create_time = time.gmtime(os.path.getctime(filepath)-time.timezone)
            md_meta['date'] = time.strftime('%Y-%m-%d %H:%M:%S', create_time)

        md_meta['mdfile'] = os.path.abspath(os.path.join(md_path, filepath))
        return dict(meta=md_meta, body=md_body)

    def check_new(self, mdfile):
        if self.db.query(Article).filter_by(mdfile=mdfile).count():
            return False
        return True

    def add_update(self, parsed_md, new_flag):
        # add new post
        if new_flag:
            a = Article(title=parsed_md['meta']['title'],
                date=parsed_md['meta']['date'],
                content=parsed_md['body'],
                mdfile = parsed_md['meta']['mdfile'],
            )
        # update post
        else:
            a = self.db.query(Article).\
                        filter_by(mdfile=parsed_md['meta']['mdfile']).one()
            a.title = parsed_md['meta']['title']
            a.date = parsed_md['meta']['date']
            a.content = parsed_md['body']
            a.mdfile = parsed_md['meta']['mdfile']

        # category
        tmp_category = self.db.query(Category).\
                        filter_by(name=parsed_md['meta']['category'])
        if tmp_category.count():
            a.category = tmp_category.one()
        else:
            a.category = Category(name=parsed_md['meta']['category'])

        # tags
        if 'tags' in parsed_md['meta']:
            for tag in parsed_md['meta']['tags']:
                tmp_tag = self.db.query(Tag).filter_by(name=tag)
                if tmp_tag.count():
                    a.tags.append(tmp_tag.one())
                else:
                    a.tags.append(Tag(name=tag))

        self.db.add(a)
        self.db.commit()

    def delete(self, mdfile):
        article = self.db.query(Article).filter_by(mdfile=mdfile).one()
        self.db.delete(article)
        self.db.commit()


if __name__ == '__main__':
    utils = Utils()
    parsed_md = utils.parse_md(os.path.join(md_path, 'test1.md'))
    utils.add_update(parsed_md, True)
