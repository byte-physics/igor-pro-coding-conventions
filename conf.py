from subprocess import Popen, PIPE

# functions
def get_version():
    """
    Returns project version as derived by git.
    """

    branchString = Popen('git rev-parse --abbrev-ref HEAD', stdout = PIPE, shell = True).stdout.read().rstrip()
    revString    = Popen('git describe --always --tags', stdout = PIPE, shell = True).stdout.read().rstrip()

    return "({branch}) {version}".format(branch=branchString.decode('ascii'), version=revString.decode('ascii'))

version = get_version()
release = version

# -- Project information -----------------------------------------------------

project = 'Igor Pro coding conventions'
copyright = '2017 - present, All contributors'
author = 'All contributors'

master_doc = "index"

html_show_sourcelink = False

# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinxcontrib.fulltoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_theme_options = {
    'fixed_sidebar': 'true',
    'page_width':'1500px'
}

html_sidebars = {
        '**': ['localtoc.html', 'searchbox.html', 'version.html'],
        }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# pygments options
highlight_language = "text"
pygments_style     = "igor"
