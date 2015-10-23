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
                Extension('yapyg/math_2d', ['yapyg/math_2d.c']),
                Extension('yapyg/math_collision', ['yapyg/math_collision.c']),
                Extension('yapyg/movers', ['yapyg/movers.c']),
                Extension('yapyg/screen', ['yapyg/screen.c']),
                Extension('yapyg/sprites', ['yapyg/sprites.c']),
                Extension('yapyg/texture_db', ['yapyg/texture_db.c']),
                Extension('yapyg/tiles', ['yapyg/tiles.c']),
                Extension('yapyg/view', ['yapyg/view.c']),
                Extension('yapyg_movers/physical_mover', ['yapyg_movers/physical_mover.c']),
                Extension('yapyg_movers/linear_mover', ['yapyg_movers/linear_mover.c']),
                Extension('yapyg_widgets/display_widget', ['yapyg_widgets/display_widget.c']),
                ]

setup(  name='yapyg',
        version='0.5.0',
        description='Yet Another Python Game Engine',
        author='Raihan Kibria',
        author_email='raihan@kibria.de',
        url='https://github.com/rkibria/yapyg',
        packages=['yapyg', 'yapyg_helpers', 'yapyg_movers', 'yapyg_viewers', 'yapyg_widgets'],
        ext_modules=ext
        )
