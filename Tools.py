# -*- coding: utf-8 -*-
import pdb

import re
import sys
import os
import os.path
from datetime import datetime
import shutil
import cPickle
import hashlib

from config import *


class Tool(object):
    @staticmethod
    def check_folders():
        '''
        Check source folder and deploy folder are existed, if not, create
        '''
        if not os.path.exists(Source_folder):
            try:
                os.makedirs(Source_folder, 0755)
            except OSError as e:
                print('Make source folder failed. Error: %s' % e)
        else:
            print('Make source folder encounter an already existed path')
            sys.exit(1)


        if not os.path.exists(Deployed_folder):
            try:
                os.makedirs(Deployed_folder, 0755)
            except OSError as e:
                print('Make deploy folder failed. Error: %s' % e)
        else:
            print('Make deploy folder encounter an already existed path')
            sys.exit(1)

    @staticmethod
    def _init_source_folder():
        pass

    @staticmethod
    def _init_deploy_folder():
        '''
        1.  Remove already existed HTML files
        2.  Copy template/css
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

        # Copy template/css to Deploy
        try:
            shutil.copytree(os.path.join(Template_path, 'css'),
                            os.path.join(Deployed_folder, 'css'))
        except shutil.Error as e:
            print('template/css copied failed. Error: %s' % e)
        except OSError as e:
            print('template/css copied failed. Error: %s' % e)

        # Copy template/js to Deploy
        try:
            shutil.copytree(os.path.join(Template_path, 'js'),
                            os.path.join(Deployed_folder, 'js'))
        except shutil.Error as e:
            print('template/js copied failed. Error: %s' % e)
        except OSError as e:
            print('template/js copied failed. Error: %s' % e)

    @staticmethod
    def init_folders():
        Tool._init_deploy_folder()


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

    @staticmethod
    def images_process(date, line):
        pattern = re.compile(r'(?P<start>!\[.*\]\()(?P<replace>.*)(?P<end>\))')
        result = pattern.search(line)
        try:
            newline = line.replace(result.group('replace'),
                                    os.path.join('/img',
                                                date,
                                                result.group('replace')))
        except:
            return line
        else:
            return newline


    @staticmethod
    def is_subpath(sub, master):
        return os.path.abspath(sub).startswith(os.path.abspath(master))
