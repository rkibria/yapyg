from os import environ
from os.path import dirname, join
from distutils.core import setup
from distutils.extension import Extension
try:
        from Cython.Build import cythonize
        have_cython = True
except ImportError:
        have_cython = False

if have_cython:
        ext = cythonize("yapyg/*.pyx") + cythonize("yapyg_movers/*.pyx") + cythonize("yapyg_widgets/*.pyx")
else:
        ext = [
                Extension('yapyg/collisions', ['yapyg/collisions.c']),
                Extension('yapyg/controls', ['yapyg/controls.c']),
                Extension('yapyg/entities', ['yapyg/entities.c']),
                Extension('yapyg/fixpoint', ['yapyg/fixpoint.c']),
                Extension('yapyg/fixpoint_2d', ['yapyg/fixpoint_2d.c']),
                Extension('yapyg/fixpoint_coll', ['yapyg/fixpoint_2d.c']),
                Extension('yapyg/fixpoint_trig', ['yapyg/fixpoint_trig.c']),
                Extension('yapyg/globals', ['yapyg/globals.c']),
                Extension('yapyg/movers', ['yapyg/movers.c']),
                Extension('yapyg/screen', ['yapyg/screen.c']),
                Extension('yapyg/sprites', ['yapyg/sprites.c']),
                Extension('yapyg/texture_db', ['yapyg/texture_db.c']),
                Extension('yapyg/tiles', ['yapyg/tiles.c']),
                Extension('yapyg/view', ['yapyg/view.c']),
                Extension('yapyg_movers/physical', ['yapyg_movers/physical.c']),
                Extension('yapyg_movers/linear', ['yapyg_movers/linear.c']),
                Extension('yapyg_widgets/display_widget', ['yapyg_widgets/display_widget.c']),
                ]

setup(  name='yapyg',
        version='0.1.0',
        description='Yet Another Python Game Engine',
        author='Raihan Kibria',
        author_email='raihan@kibria.de',
        url='https://github.com/rkibria/yapyg',
        packages=['yapyg', 'yapyg_helpers', 'yapyg_movers', 'yapyg_viewers', 'yapyg_widgets'],
        ext_modules=ext
        )
