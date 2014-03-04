# -*- coding: utf-8 -*-

import sys
import os
import os.path
from datetime import datetime
import shutil

from config import *

class Tool(object):
    def __init__(self):
        #self.writer = Writer()
        pass

    def check_folders(self):
        '''
        Check source folder and deploy folder are existed, if not, create
        '''
        if not os.path.exists(Source_folder):
            try:
                os.mkdir(Source_folder)
            except OSError as e:
                print('Make source folder failed. Error: %s' % e)
        else:
            print('Make source folder encounter an already existed path')
            sys.exit(1)


        if not os.path.exists(Deployed_folder):
            try:
                os.mkdir(Deployed_folder)
            except OSError as e:
                print('Make deploy folder failed. Error: %s' % e)
        else:
            print('Make deploy folder encounter an already existed path')
            sys.exit(1)

    def _init_source_folder(self):
        '''
        Generates HTML by all the Markdown files
        '''
        for path in os.listdir(Source_folder):
            if os.path.isfile(path) and\
            path.split('.')[-1] in Markdown_extensions:
                #self.writer.generate_article(path)
        #self.writer.generate_index()
        #self.writer.generate_page()
                pass

    def _init_deploy_folder(self):
        '''
        1.  Remove already existed HTML files
        2.  Copy template/js, template/css
        '''
        # Remove already existed HTML file in Deploy folder
        for path in os.listdir(Deployed_folder):
            if path.split('.')[-1] in HTML_extensions:
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                    except OSError as e:
                        print('Delete file in deploy folder failed. Error: %s' % e)
            if path == 'css' or path == 'js':
                if os.path.isdir(path):
                    try:
                        os.removedirs(path)
                    except OSError as e:
                        print('Delete path in deploy folder failed. Error: %s' % e)

        # Copy template/css, template/js to Deploy
        try:
            shutil.copytree(os.path.join(Template_path, 'css'),
                            os.path.join(Deployed_folder, 'css'))
        except shutil.Error as e:
            print('template/css copied failed. Error: %s' % e)
        except OSError as e:
            print('template/css copied failed. Error: %s' % e)

        #try:
        #    shutil.copytree(os.path.join(Template_path, 'js'),
        #                    os.path.join(Deployed_folder, 'js'))
        #except shutil.Error as e:
        #    print('template/js copied failed. Error: %s' % e)
        #except OSError as e:
        #    print('template/js copied failed. Error: %s' % e)

    def init_folders(self):
        '''
        It's important that must init deploy folder first, or all the HTML files
        generates from source folder will be remove too.
        '''
        self._init_deploy_folder()
        self._init_source_folder()


class Utils(object):
    @staticmethod
    def to_unicode(value):
        if isinstance(value, unicode):
            return value
        if isinstance(value, basestring):
            return value.decode('utf-8')
        if isinstance(value, int):
            return str(value)
        if isinstance(value, bytes):
            return value.decode('utf-8')
        return value

    @staticmethod
    def to_utf8(value):
        if isinstance(value, (bytes, type(None), str)):
            return value
        if isinstance(value, int):
            return str(value)
        assert isinstance(value, unicode)
        return value.encode('utf-8')

    @staticmethod
    def to_time(timetuple):
        return datetime.strftime(timetuple, '%Y-%m-%d')

    @staticmethod
    def parse_time(value):
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, float):
            return datetime.fromtimestamp(value)
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            print('Unrecorgnized time format. Error: %s' % e)



if __name__ == '__main__':
    tool = Tool()
    tool.check_folders()
    tool.init_folders()
