# -*- coding: utf-8 -*-

documentation = {}
documentation['init'] = '''
    Create Needed folders

    # Project folder:
        cli.py
        config.py
        Writer.py
        template/
            Index.html
            Page.html
            Article.html
            css/
                style.css
            js/
                main.js
            

    # Source folder
        data.pickle # {inode: hash(mdcontent)}
        article1.md
        article2.md
        ...

    # Deployed folder:
        Index.html
        page/
            page1.html
            page2.html
            ...
        article1.html
        article2.html
        ...
        css/
            style.css
        js/
            main.js
'''
documentation['watch'] = '''
    Start a pyinofity thread which is watching the source folder
'''
