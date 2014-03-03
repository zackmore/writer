# -*- coding: utf -*-
import pdb

import os
import os.path
import time
import re
import urllib

import markdown2
from jinja2 import Environment, FileSystemLoader

from Tools import *
from config import *

class Writer(object):
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(Template_path))
        self.page_quantity = Page_quantity

    def _sort_articles(self, quantity='all'):
        '''
        Sort the html files in /Deploy
        '''
        htmls = [html for html in os.listdir(Deployed_folder)\
                        if html.split('.')[-1] in HTML_extensions]
        date_htmls = []
        for html in htmls:
            file_date = '-'.join(html.split('-')[:3])
            file_name = '-'.join(html.split('-')[3:])
            date_htmls.append(tuple([file_date, file_name]))


        date_htmls.sort(reverse=True)
        if Page_sort == 'asc':
            date_htmls.sort()

        if quantity == 'all':
            return date_htmls
        elif isinstance(quantity, int):
            if quantity >= len(date_htmls):
                return date_htmls
            else:
                return date_htmls[:quantity]


    def generate_index(self):
        '''
        Index the newest 10 articles
        '''
        pass

    def generate_page(self, articles):
        '''
        Write to /Deploy/page/ path
        '''
        pages = len(articles) / self.page_quantity
        if len(articles) % self.page_quantity > 0:
            pages =+ 1
        if pages > 1:
            if not os.path.exists(os.path.join(Deployed_folder, 'page')):
                try:
                    os.mkdir(os.path.join(Deployed_folder, 'page'))
                except IOError as e:
                    print('Create page folder failed. Error: %s' % e)

        if not os.path.exists(os.path.join(Deployed_folder, 'page')):
            os.mkdir(os.path.join(Deployed_folder, 'page'))

        template = self.env.get_template('page.html')
        for page in xrange(pages):
            page_url = os.path.join(Deployed_folder, 'page', str(page+1)+'.html')
            try:
                f = open(page_url, 'w')
                items_list = []
                for d in articles[page*self.page_quantity:(page+1)*self.page_quantity]: 
                    tmp_item = {}
                    tmp_item['date'] = d[0]
                    tmp_item['title'] = d[1]
                    tmp_item['url'] = tmp_item['date'] + '-' + tmp_item['title']
                    items_list.append(tmp_item)
                f.write(template.render(item_list=items_list, page_number=page+1))
                f.close()
            except IOError as e:
                print('Create page.html file failed. Error: %s' % e)

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

        result['url'] = urllib.quote_plus('-'.join([result['date'], re.sub(r'\s+', '-', result['title'])]))

        return result

    def generate_article(self, filepath):
        html = self._parse_md(filepath)
        template = self.env.get_template('article.html')
        try:
            f = open(os.path.join(Deployed_folder, html['url']+'.html'), 'w')
            f.write(template.render(article=html))
            f.close()
        except IOError as e:
            print('Build article failed. Error: %s' % e)


if __name__ == '__main__':
    writer = Writer()
    writer.generate_article('/tmp/Sources/1.md')
    writer.generate_page(writer._sort_articles())
    #writer.generate_article('/tmp/Sources/2.md')
    #writer.generate_article('/tmp/Sources/3.md')
    #writer.generate_article('/tmp/Sources/4.md')
    #writer._sort_articles()
