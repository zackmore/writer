# -*- coding: utf-8 -*-

import os.path

Blog_name = 'Zlog'
Blog_url = 'http://zengq.in/'

Article_folder = '/home/zack/Workspace/Git/writer/Articles/'
Source_folder = os.path.join(Article_folder, 'Source')
Deployed_folder = os.path.join(Article_folder, 'Deploy')

Remote_server = 'devio.us'
Remote_server_port = '22'
Remote_server_user = 'zulius'
Remote_server_path = '/home/zulius/public_html/blog/'

Template_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                'template'))

# The items quantity of one page
Page_sort = 'desc' # 'desc' or 'asc'
Index_quantity = 10
Page_quantity = 10 
Feed_quantity = 10

Image_extensions = ['jpg', 'jpeg', 'png', 'gif']
HTML_extensions = ['html', 'htm', 'shtml', 'cshtml', 'xhtml']
Markdown_extensions = ['markdown', 'mdown', 'mkdn', 'md', 'mkd',
                    'mdwn', 'mdtxt', 'mdtext', 'text']
