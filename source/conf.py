# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Fehlersuche bei IKEv2 IPsec VPN'
copyright = '2020, Mathias Weidner'
author = 'Mathias Weidner'

# The short X.Y version
version = '0.1'
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib.bibtex',
    'sphinx.ext.todo',
    'sphinx.ext.autosectionlabel',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'de'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'FehlersuchebeiIKEv2IPsecVPNdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_additional_files = [ 'images/by-sa.pdf' ]

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'paperheight=7in,paperwidth=9.1in',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '11pt',

    'fncychap': '',
    # Additional stuff for the LaTeX preamble.
    #
    'preamble': r'''
\usepackage{chngcntr}
\makeatletter
\fancypagestyle{normal}{%
\fancyhf{}%
\fancyhead[LE]{{\em\nouppercase{\leftmark}}}%
\fancyhead[RO]{{\em\nouppercase{\rightmark}}}%
\fancyfoot[LE,RO]{{\em\thepage}}%
\renewcommand{\headrulewidth}{0pt}%
\renewcommand{\footrulewidth}{0pt}%
}
\fancypagestyle{plain}{%
\fancyhf{}%
\fancyhead[LE,RO]{}
\fancyfoot[LE,RO]{{\em\thepage}}%
\renewcommand{\headrulewidth}{0pt}%
\renewcommand{\footrulewidth}{0pt}%
\makeatother
}
\geometry{%
papersize={7.5in,9.25in},%
height={36\baselineskip},%
hdivide={1.0in,*,1.0in},%
vdivide={1.2in,*,*}
}
%% nur was im Inhaltsverzeichnis auftaucht, wird nummeriert
\setcounter{secnumdepth}{1}
\hyphenation{
    Bug-reports
	da-rauf
    WireShark
}
\def\sphinxstyleindexentry   #1{{#1}}
''',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
    'maketitle': r'''
%\titlehead{This is the titlehead}
%\subject{This is the subject}
%\subtitle{This is the subtitle}
%\author{This is the author with a footnote\thanks{Footnote to author}}
%\date{21.12.2018}
%\publishers{These are the publishers}
%\extratitle{\centering This is the extra title}
\uppertitleback{
\textbf{Fehlersuche bei IKEv2 IPsec VPN}

\textcopyright~Mathias Weidner, 2020

\vspace{1cm}
\textbf{ISBN:} 9798574888759 (Papierversion)
}
\lowertitleback{
Aktuelle Informationene zu diesem Buch finden sich unter
\url{http://buecher.mamawe.net/}.

\vspace{1cm}
\includegraphics[width=3cm,angle=0]{by-sa.pdf}

Dieses Werk ist unter einer Creative Commons Lizenz vom Typ
Namensnennung - Weitergabe unter gleichen Bedingungen 4.0 International
zugänglich.
Um eine Kopie dieser Lizenz einzusehen,
konsultieren Sie \url{http://creativecommons.org/licenses/by-sa/4.0/}
oder wenden Sie sich brieflich
an Creative Commons, Postfach 1866, Mountain View, California, 94042, USA.
}
%\lowertitleback{The lower part of the backtitle}
%\dedication{This sample is dedicated to all unsuccessful trials so far}
\maketitle
''',
   'releasename': '',
}

latex_docclass = {
   'manual': 'scrbook',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'FehlersuchebeiIKEv2IPsecVPN.tex', 'Fehlersuche bei IKEv2 IPsec VPN',
     'Mathias Weidner', 'manual'),
]

latex_use_xindy = True;

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'fehlersuchebeiikev2ipsecvpn', 'Fehlersuche bei IKEv2 IPsec VPN',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'FehlersuchebeiIKEv2IPsecVPN', 'Fehlersuche bei IKEv2 IPsec VPN',
     author, 'FehlersuchebeiIKEv2IPsecVPN', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

numfig = True

autosectionlabel_prefix_document = True

# vim: set sw=4 ts=4 et:
