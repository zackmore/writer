# -*- coding: utf-8 -*-

import os.path

Blog_name = 'Zlog'

Source_folder = '/tmp/Sources'
Deployed_folder = '/tmp/Deploy'

Template_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                'template'))

# The items quantity of one page
Page_sort = 'desc' # 'desc' or 'asc'
Index_quantity = 1
Page_quantity = 1 

Image_extensions = ['jpg', 'jpeg', 'png', 'gif']
HTML_extensions = ['html', 'htm', 'shtml', 'cshtml', 'xhtml']
Markdown_extensions = ['markdown', 'mdown', 'mkdn', 'md', 'mkd',
                    'mdwn', 'mdtxt', 'mdtext', 'text']
