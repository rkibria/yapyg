#!/bin/bash

VERSION_yapyg=${VERSION_yapyg:-master}
URL_yapyg=http://github.com/rkibria/yapyg/zipball/$VERSION_yapyg/yapyg.zip
DEPS_yapyg=(python kivy)
MD5_yapyg=
BUILD_yapyg=$BUILD_PATH/yapyg/$(get_directory $URL_yapyg)
RECIPE_yapyg=$RECIPES_PATH/yapyg

function prebuild_yapyg() {
	true
}

function build_yapyg() {

	cd $BUILD_yapyg

	push_arm

        export LDFLAGS="$LDFLAGS -L$LIBS_PATH"
	export LDSHARED="$LIBLINK"

	try find . -iname '*.pyx' -exec $CYTHON {} \;
	try $HOSTPYTHON setup.py build_ext -v
	try find build/lib.* -name "*.o" -exec $STRIP {} \;

	export PYTHONPATH=$BUILD_hostpython/Lib/site-packages
	try $BUILD_hostpython/hostpython setup.py install -O2 --root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages

	unset LDSHARED
        
	pop_arm
}

function postbuild_yapyg() {
	true
}
