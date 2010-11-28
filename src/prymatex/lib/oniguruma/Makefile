# Oniguruma Makefile for Python wrapper
#
#

PLATFORM=$(shell python -c "import sys; print(sys.platform)")

.PHONY:  pyrex re clean defs

all: cython


cython: pyonig.so

pyonig.c: pyonig.pyx oniguruma_consts.py
	cython pyonig.pyx


oniguruma_consts.py: includes/oniguruma.h
	@echo "Converting .H defs to python"
	./h2cython.py -v -r "^ONIG_" -o $@ $^

%.o: %.c
	gcc -c -fPIC -I/usr/include/python2.6 $^ -o $@

pyonig.so: pyonig.o
	gcc -shared $^ -lonig -o $@
	@echo "-----------------------------------------------------------"
	@echo "You should be able to make import pyoing and play with it :)"
	@echo "-----------------------------------------------------------"

clean:
	@rm -rf pyonig.so pyonig.o pyonig.c pyonig.pxd oniguruma_consts.py

re:	clean all

test: all
	@echo "Testing Oniguruma Binding, you should see onig version and copyrigh message"
	@python -c "import pyonig; print pyonig.VERSION; print pyonig.COPYRIGHT"

