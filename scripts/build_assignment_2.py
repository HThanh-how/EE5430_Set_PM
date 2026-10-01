"""Compatibility entry point for the revised LaTeX reports."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name('build_assignment_2_latex.py')), run_name='__main__')
