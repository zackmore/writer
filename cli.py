# -*- coding: utf-8 -*-

documentation = {}

documentation['help'] = '''Writer
    writer init
    writer watch
    writer watch --stop
    writer help
'''  

documentation['init'] = '''
    -   Read settings from config.py
    -   Create the 2 folders if needed
    -   Check if there is md files already existed in source folder
    -   Generate the html files (will remove all the existed html files first)


    # Project folder:
        cli.py      (command line)
        config.py   (including options)
        Tools.py    (cli.py invoke this file)
        Writer.py   (.md to .html, and output page/index.html)
        template/
            Index.html
            Page.html
            Article.html
            css/
                style.css
            js/
                main.js
            

    # Source folder
        article1.md
        article2.md
        ...

    # Deployed folder:
        Index.html
        page/
            1.html
            2.html
            ...
        article1.html
        article2.html
        ...
        css/
            style.css
        js/
            main.js
'''

#documentation['watch']['start'] = '''
#    Start a pyinofity thread which is watching on the source folder
#'''
#
#documentation['watch']['stop'] = '''
#    Stop the pyinofity thread
#'''

def main():
    print(documentation['help'])


if __name__ == '__main__':
    main()
