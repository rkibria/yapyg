from os import environ
from os.path import dirname, join
from distutils.core import setup
from distutils.extension import Extension
try:
    from Cython.Distutils import build_ext
    have_cython = True
except ImportError:
    have_cython = False

if have_cython:
    yapyg_files = [
        'fixpoint.pxi',
        ]
    cmdclass = {'build_ext': build_ext}
else:
    yapyg_files = ['fixpoint.c']
    cmdclass = {}

ext = Extension('yapyg',
    yapyg_files,
    extra_compile_args=['-std=c99', '-ffast-math', '-fPIC'])
 
if environ.get('READTHEDOCS', None) == 'True':
    ext.pyrex_directives = {'embedsignature': True}

setup(
    name='yapyg',
    description='Cython bindings for yapyg',
    author='Raihan Kibria',
    author_email='raihan@kibria.de',
    cmdclass=cmdclass,
    ext_modules=[ext])
