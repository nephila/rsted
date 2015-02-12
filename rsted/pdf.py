
import os
from os.path import join as J
import tempfile
import subprocess
import shutil


def rst2pdf(rst_txt):
    if not rst_txt.strip():
        return "<html/>"

    with tempfile.TemporaryDirectory() as tmpdir:
        copy_src = os.path.join(os.path.dirname(__file__), '..', 'sphinx')
        copy_dst = os.path.join(tmpdir, 'sphinx')
        rst_fname = os.path.join(copy_dst, 'index.rst')
        tex_fname = os.path.join(copy_dst, 'sphinxed.tex')
        pdf_fname = os.path.join(copy_dst, 'sphinxed.pdf')
        cmd1_args = "sphinx-build -b latex  . .".split()
        cmd2_args = ["pdflatex", tex_fname]
    
        shutil.copytree(copy_src, copy_dst)
        with open(rst_fname, "w", encoding="utf-8") as fout_rst:
            fout_rst.write(rst_txt)
        
        subprocess.check_output(cmd1_args, cwd=copy_dst)
        subprocess.check_output(cmd2_args, cwd=copy_dst)
        
        with open(pdf_fname, 'rb') as fin_pdf:
            pdf = fin_pdf.read()
            
        return pdf


