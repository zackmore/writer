#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
import shlex

from config import *
from Tools import *
from Writer import *


documentation = {}
documentation['help'] = '''Writer
    writer init                                 Create the needed path
    writer build [test] [filepath, ...]         Build Html(s)
    writer pull                                 Get Source and Deploy from your server
    wrtier push                                 Push your Source and Deploy to your server
    writer help                                 Show this information
'''  

documentation['init'] = '''
Usage: python cli.py init

1.  Read settings from config.py
2.  Create the 2 folders if needed
3.  Copy template to Deployed_folder
'''

documentation['build'] = '''
Usage: python cli.py build [filepath, ...]

Change all Markdown files in Source folder to HTML files in Deploy folder. If filepath offered, will check if it is in Source folder, if not, will move the file in Source and then change.
'''

documentation['test'] = '''
Usage: python cli.py test [filepath, ...]

Check if there is any possible will replace the existed articles.
'''

documentation['push'] = '''
Usage: python cli.py push

Push your Source and Deploy to your server
'''

documentation['pull'] = '''
Usage: python cli.py pull

Get Source and Deploy from your server
'''

def main():
    command = 'help'

    if len(sys.argv[1]):
        command = sys.argv[1]

    if command == 'help':
        if not sys.argv[2]:
            print(documentation['help'])
        elif sys.argv[2] == 'init':
            print(documentation['init'])
        elif sys.argv[2] == 'build':
            print(documentation['build'])

    if command == 'init':
        Tool.check_folders()
        Tool.init_folders()

    if command == 'test':
        if len(sys.argv[2:]):
            for path in sys.argv[2:]:
                if not Utils.is_subpath(path, Source_folder):
                    shutil.move(path, Source_folder)

        all_mds = [os.path.join(Source_folder, x) for x in os.listdir(Source_folder)\
                       if x.split('.')[-1] in Markdown_extensions or os.path.isdir(os.path.join(Source_folder, x))]
        conflict = []
        for path in all_mds:
            post = Post(os.path.join(Source_folder, path))
            if os.path.exists(os.path.join(Deployed_folder, post.htmlfile)):
                conflict.append(post)

        if len(conflict):
            for p in conflict:
                print('%s will be conflicted.[%s]' % (p.htmlfile, p.filepath))
        else:
            print('No conflict.')

    if command == 'build':
        if len(sys.argv[2:]):
            for path in sys.argv[2:]:
                if not Utils.is_subpath(path, Source_folder):
                    shutil.move(path, Source_folder)

        all_mds = [os.path.join(Source_folder, x) for x in os.listdir(Source_folder)\
                       if x.split('.')[-1] in Markdown_extensions or os.path.isdir(os.path.join(Source_folder, x))]
        postlist = []
        for path in all_mds:
            post = Post(os.path.join(Source_folder, path))
            post.to_html()
            postlist.append(post)
        page = Page(postlist)
        page.to_pagehtml()
        page.to_indexhtml()
        page.to_feedxml()

    if command == 'push' or command == 'pull':
        local = Article_folder
        server = Remote_server_user + '@' + Remote_server + ':' + Remote_server_path

        if not os.path.exists(local):
            try:
                os.makedirs(local, 0755)
            except IOError as e:
                print('Create local Article folder failed. Error: %s' % e)

        if not server.endswith('/'):
            server += '/'
        if not local.endswith('/'):
            local += '/'

        sub_command = 'rsync -aP -e "ssh -p %s" ' % Remote_server_port

        if command == 'push':
            sub_command += local + ' ' + server
        if command == 'pull':
            sub_command += server + ' ' + local

        subprocess.call(shlex.split(sub_command))


if __name__ == '__main__':
    main()
