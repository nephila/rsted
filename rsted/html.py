
import os
from os.path import join as J
import tempfile
import subprocess
from subprocess import Popen
import shutil
#import codecs

#utf8codec = codecs.lookup('utf-8')

# see http://docutils.sourceforge.net/docs/user/config.html
default_rst_opts = {
    'no_generator': True,
    'no_source_link': True,
    'tab_width': 4,
    'file_insertion_enabled': False,
    'raw_enabled': False,
    'stylesheet_path': None,
    'traceback': True,
    'halt_level': 5,
}

def _rst2html(rst_txt):
    with tempfile.TemporaryDirectory() as tmpdir:
        copy_src = os.path.join(os.path.dirname(__file__), '..', 'sphinx', 'conf.py')
        rst_fname = os.path.join(tmpdir, 'index.rst')
        htm_fname = os.path.join(tmpdir, 'index.html')
        cmd_args = "sphinx-build -b html  . .".split()

        shutil.copy(copy_src, tmpdir)
        with open(rst_fname, "w", encoding="utf-8") as fout_rst:
            fout_rst.write(rst_txt)
        
        subprocess.check_call(cmd_args, cwd=tmpdir)
        #with Popen(cmd_args, cwd=tmpdir):
        
        with open(htm_fname, encoding="utf-8") as fin_html:
            html = fin_html.read()
            
        return html
        
    
def rst2html(rst, theme=None, opts=None):
    rst_opts = default_rst_opts.copy()
    if opts:
        rst_opts.update(opts)
    rst_opts['template'] = 'var/themes/template.txt'

    stylesheets = ['basic.css']
    if theme:
        stylesheets.append('%s/%s.css' % (theme, theme))
    rst_opts['stylesheet'] = ','.join([J('var/themes/', p) for p in stylesheets ])

    if rst.strip():
        out = _rst2html(rst)
    else:
        out = "<html/>"
    return out

