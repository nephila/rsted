#! python3
# -*- coding: utf-8 -*-


import sys, os, io

proj_ver = "0.0.1"
mydir = os.path.dirname(__file__)

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.extlinks',
    #'matplotlib.sphinxext.plot_directive',
]

#templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'sphined_generated'
copyright = '2013-2015, European Commission (JRC), EUPL 1.1+'  # @ReservedAssignment

version = proj_ver
release = proj_ver

extlinks = {
#     'issue': ('https://github.com/ankostis/wltp/issues/%s','issue')
}

exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'obj'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, keep warnings as "system message" paragraphs in the built documents.
keep_warnings = True

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "sphined generated"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    '**': []
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = False

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
#    'jsonschema': ('http://python-jsonschema.readthedocs.org/en/latest/', None),
}


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',
'papersize': 'a4paper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
'preamble': u'''
    \\usepackage{amsmath}
''',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'sphinxed.tex', 'Sphinxed generated',
   "Anyone' section", 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True



def setup(app):
    pass
