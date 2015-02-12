
import os
from os.path import join as J
import tempfile
import subprocess
import shutil


def rst2pdf(rst_txt, theme=None, opts=None):
    if not rst_txt.strip():
        return "<html/>"

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
        

