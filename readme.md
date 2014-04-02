# writer

Yet another static blog generator. A simple tool that can turn  markdown files to html files, and put them directly at the server root path. And it also very simple: only pagination, no category/tags support, no additional increment build.

## Quick Start

1.  Edit `config.py`
2.  `python cli.py init`
3.  Put your md file or directory (including a markdown file and images) in Source_folder
4.  `python cli.py build`
5.  `python cli.py push`

## Usage

-   `python cli.py init`

    Created needed paths

-   `python cli.py build [filepath, filepath, ...]`

    Build Htmls

-   `python cli.py test [filepath, filepath, ...]`

    Check for build results

-   `python cli.py push`

    Push your Source and Deploy to your server

-   `python cli.py pull`

    Get Source and Deploy from your server

-   `python cli.py help`

    Show help information

## Documentation

Basically the `Writer.py` is for all things about pages, the `Tools.py` is for other addtional functions.

When you `python cli.py init`, follows will happen:

-   Read settings from config.py
-   Create the 2 folders if needed
-   Check if there is md files already existed in source folder
-   Generate the html files (will remove all the existed html files first)

A valid source file should be like this:

```
Title: Your article title
Date: YYYY-mm-dd
Description: some words

================ (or '-------------', at least 3 characters)

And here goes the markdown format content.
```

The `Title` `Date` `Description` are all optional. `Description` will be an empty string if not set; `Date` will be the **first** build time and its format is also `YYYY-mm-dd`; `Title` will be as `YYYY-mm-dd-sourcefilename` is not set. I recommand you should set all the 'header' information manually for a better content control.

## Todo

-   multi-build
-   comment Disqus
