# -*- coding: utf-8 -*-

import os.path

Blog_name = ''
Blog_url = ''

Article_folder = ''
Source_folder = os.path.join(Article_folder, 'Source')
Deployed_folder = os.path.join(Article_folder, 'Deploy')

Remote_server = ''
Remote_server_port = ''
Remote_server_user = ''
Remote_server_path = ''

Template_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                'template'))

Page_sort = 'desc' # 'desc' or 'asc'
Index_quantity = 10
Page_quantity = 10 
Feed_quantity = 10

Image_extensions = ['jpg', 'jpeg', 'png', 'gif']
HTML_extensions = ['html', 'htm', 'shtml', 'cshtml', 'xhtml']
Markdown_extensions = ['markdown', 'mdown', 'mkdn', 'md', 'mkd',
                    'mdwn', 'mdtxt', 'mdtext', 'text']
