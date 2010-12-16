# Oniguruma Makefile for Python wrapper
#
#

PLATFORM=$(shell python -c "import sys; print(sys.platform)")
CYTHONARGS=-v

.PHONY:  pyrex re clean defs consts consts_clean consts_re

all: cython


cython: pyonig.so

pyonig.c: pyonig.pyx oniguruma_consts.py  h2cython.py
	cython ${CYTHONARGS} pyonig.pyx


oniguruma_consts.py: includes/oniguruma.h h2cython.py
	@echo "Converting .H defs to python"
	./h2cython.py -v -r "^ONIG_" -f -o $@ includes/oniguruma.h
	
consts: oniguruma_consts.py
	
consts_clean:
	rm oniguruma_consts.py
	
consts_re: consts_clean oniguruma_consts.py
	

%.o: %.c
	gcc -c -fPIC -I/usr/include/python2.6 $^ -o $@

pyonig.so: pyonig.o
	gcc -shared $^ -lonig -o $@
	@echo "-----------------------------------------------------------"
	@echo "You should be able to make import pyoing and play with it :)"
	@echo "-----------------------------------------------------------"

clean:
	@rm -rf pyonig.so pyonig.o pyonig.c pyonig.pxd oniguruma_consts.py oniguruma_synenc.pxd

re:	clean all

test: all
	@echo "Testing Oniguruma Binding, you should see onig version and copyrigh message"
	@python -c "import pyonig; print pyonig.VERSION; print pyonig.COPYRIGHT"

