# writer

Yet another static blog generator. I just need a simple tool that can turn my markdown files to html files, and put them directly at the server root path. And also my requirements are very simple at first: only pagination, no category/tags support, no additional increment build. But these features will be implement later.

## Usage

-   `python cli.py init`

    Created needed paths

-   `python cli.py build [-p] [filepath, filepath, ...]`

    Build Htmls

-   `python cli.py help`

    Show help information

## Documentation

Basically the `Writer.py` is for all things about pages, the `Tools.py` is for other addtional functions.

When you `python cli.py init`, follows will happen:

-   Read settings from config.py
-   Create the 2 folders if needed
-   Check if there is md files already existed in source folder
-   Generate the html files (will remove all the existed html files first)

it will generates some paths just like below:

```
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

# Source folder
    article1.md
    article2.md
    ...

# Deployed folder:
    index.html
    page/
        1.html
        2.html
        ...
    article1.html
    article2.html
    ...
    css/
        style.css
```


## Todo

-   images Dropbox
-   comment Disqus
-   Remote Sync local Deploy and server Deploy
-   category/tags support
-   additional increment build (with SQLite)
-   Source Folder monitor
