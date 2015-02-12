
import os
from os.path import join as J
import tempfile
import subprocess
import shutil
import re
import logging

regex_html = re.compile('<html.*</html>', re.DOTALL)

def rst2html(rst_txt):
    if not rst_txt.strip():
        return "<html/>"

    with tempfile.TemporaryDirectory() as tmpdir:
        #tmpdir = '/tmp/t1'
        copy_src = os.path.join(os.path.dirname(__file__), '..', 'sphinx')
        copy_dst = os.path.join(tmpdir, 'sphinx')
        rst_fname = os.path.join(copy_dst, 'index.rst')
        htm_fname = os.path.join(copy_dst, 'index.html')
        cmd_args = "sphinx-build -b singlehtml  . .".split()
    
        shutil.copytree(copy_src, copy_dst)
        with open(rst_fname, "w", encoding="utf-8") as fout_rst:
            fout_rst.write(rst_txt)
        
        out = subprocess.check_output(cmd_args, cwd=copy_dst)
        logging.log(logging.INFO, out.decode('utf-8'))
        
        with open(htm_fname, encoding="utf-8") as fin_html:
            html = fin_html.read()
            
        m = regex_html.search(html)
        if m:
            return m.group(0)
        return html


