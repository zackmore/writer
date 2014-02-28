# -*- coding: utf -*-
import pdb

import os
import os.path
import time
import re
import urllib

import janja2
import markdown2

from Tools import *
from config import *

class Writer(object):
    def __init__(self):
        self.page_quantity = Page_Quantity

    def _list_page_output(self):
        pass

    def generate_index(self):
        '''
        Index the newest 10 articles
        '''
        pass

    def generate_page(self):
        '''
        '''
        pass

    def _parse_md(self, filepath):
        '''
        return
        {
            'url':,
            'title':,
            'date':,
            'description':,
            'content':,
        }
        '''
        file_stat = {}
        file_stat['file'] = '.'.join(os.path.basename(filepath).split('.')[:-1])
        file_stat['mtime'] = time.strftime('%Y-%m-%d',
                                        time.gmtime(os.stat(filepath).st_mtime))

        result = {}

        f = open(filepath)
        header = ''
        body = ''
        header_flag = True
        for line in f:
            if header_flag and\
                (line.startswith('---') or line.startswith('===')):
                header_flag = False
            elif header_flag:
                header += Utils._to_unicode(line)
            else:
                body += Utils._to_unicode(line)
        f.close()

        headers = header.split('\n')
        for info in headers:
            if info.startswith('Title:'):
                result['title'] = info.split(':', 1)[1].strip()
            if info.startswith('Date:'):
                result['date'] = info.split(':', 1)[1].strip()
            if info.startswith('Description:'):
                result['description'] = info.split(':', 1)[1].strip()

        result['content'] = markdown2.markdown(body, extras=['code-friendly',
                                                        'fenced-code-blocks'])

        if 'title' not in result:
            result['title'] = file_stat['file']
        if 'date' not in result:
            result['date'] = file_stat['mtime']

        result['url'] = '-'.join([result['date'], re.sub(r'\s+', '-', result['title'])])

        return result

    def generate_article(self):
        '''
        '''
        pass


if __name__ == '__main__':
    writer = Writer()
    writer._parse_md('1.md')
