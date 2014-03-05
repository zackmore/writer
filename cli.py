# -*- coding: utf-8 -*-

import sys
from Tools import *
from Writer import *

documentation = {}
documentation['help'] = '''Writer
    writer init                         Create the needed path
    writer build [filepath, ...]        Build Html(s)
    writer help                         Show this information
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
    if command == 'build':
        if len(sys.argv[2:]):
            for path in sys.argv[2:]:
                if not Utils.is_subpath(path, Source_folder):
                    shutil.move(path, Source_folder)

        all_mds = [a for a in os.listdir(Source_folder)\
                    if a.split('.')[-1] in Markdown_extensions]
        postlist = []
        for path in all_mds:
            post = Post(os.path.join(Source_folder, path))
            post.to_html()
            postlist.append(post)
        page = Page(postlist)
        page.to_pagehtml()
        page.to_indexhtml()

if __name__ == '__main__':
    main()
