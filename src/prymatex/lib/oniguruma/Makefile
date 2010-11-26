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
	./h2cython.py -o $@ $^

%.o: %.c
	gcc -c -fPIC -I/usr/include/python2.6 $^ -o $@

pyonig.so: pyonig.o
	gcc -shared $^ -lonig -o $@

clean:
	@rm -rf pyonig.so pyonig.o pyonig.c pyonig.pxd oniguruma_consts.py

re:	clean all


