# -*- coding: utf -*-
import pdb

import os
import os.path
import time
import re
import urllib
import codecs

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
        if 'index.html' in htmls:
            htmls.remove('index.html')

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


    def generate_index(self, articles):
        '''
        Index the newest 10 articles
        '''
        template = self.env.get_template('index.html')
        items_list = []
        try:
            f = open(os.path.join(Deployed_folder, 'index.html'), 'w')
            for a in articles[:Index_quantity]:
                tmp_item = {}
                date_tmp = time.strptime(a[0], '%Y-%m-%d')
                tmp_item['date'] = {}
                tmp_item['date']['year'] = time.strftime('%Y', date_tmp)
                tmp_item['date']['monthday'] = time.strftime('%m.%d', date_tmp)
                tmp_item['title'] = a[1]
                tmp_item['url'] = a[0] + '-' + a[1]
                items_list.append(tmp_item)
            f.write(template.render(articles=items_list))
            f.close()
        except IOError as e:
            print('Create index.html file failed. Error: %s' % e)

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
                    date_tmp = time.strptime(d[0], '%Y-%m-%d')
                    tmp_item['date'] = {}
                    tmp_item['date']['year'] = time.strftime('%Y', date_tmp)
                    tmp_item['date']['monthday'] = time.strftime('%m.%d', date_tmp)
                    tmp_item['title'] = d[1]
                    tmp_item['url'] = d[0] + '-' + d[1]
                    items_list.append(tmp_item)
                f.write(template.render(articles=items_list, page_number=page+1))
                f.close()
            except IOError as e:
                print('Create page.html file failed. Error: %s' % e)

    def _parse_md(self, filepath, withcontent=True):
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
                header += line
            else:
                body += line
        f.close()

        headers = [Utils._to_unicode(info) for info in header.split('\n') if info]
        for info in headers:
            if info.startswith('Title:'):
                result['title'] = info.split(':', 1)[1].strip()
            if info.startswith('Date:'):
                result['date'] = info.split(':', 1)[1].strip()
            if info.startswith('Description:'):
                result['description'] = info.split(':', 1)[1].strip()

        if withcontent:
            result['content'] = Utils._to_unicode(markdown2.markdown(body,
                                    extras=['code-friendly',
                                            'fenced-code-blocks']))

        if 'title' not in result:
            result['title'] = Utils._to_unicode(file_stat['file'])
        if 'date' not in result:
            result['date'] = Utils._to_unicode(file_stat['mtime'])

        result['htmlfile'] = '-'.join(
                                [
                                    Utils._utf8(result['date']),
                                    re.sub(r'\s+', '-', Utils._utf8(result['title']))
                                ]
                            ) + '.html'
        result['url'] = urllib.quote_plus(result['htmlfile'])

        return result

    def generate_article(self, filepath):
        html = self._parse_md(filepath)
        template = self.env.get_template('article.html')
        try:
            #f = open(os.path.join(Deployed_folder, html['url']), 'w', 'utf-8')
            f = codecs.open(os.path.join(Deployed_folder, html['htmlfile']), 'w', 'utf-8')
            f.write(template.render(article=html))
            f.close()
        except IOError as e:
            print('Build article failed. Error: %s' % e)


if __name__ == '__main__':
    writer = Writer()
    writer.generate_article(u'/tmp/Sources/中文2.md')
    #writer.generate_index(writer._sort_articles());
    #writer.generate_page(writer._sort_articles());
    #writer.generate_article('/tmp/Sources/2.md')
    #writer.generate_article('/tmp/Sources/3.md')
    #writer.generate_article('/tmp/Sources/4.md')
    #writer._sort_articles()
